#include "dimmwitted.h"
#include "assert.h"
#include "bin2text.h"
#include "binary_format.h"
#include "numa_nodes.h"
#include "common.h"
#include "factor_graph.h"
#include "gibbs_sampler.h"
#include "text2bin.h"

#include <fstream>
#include <iomanip>
#include <map>
#include <unistd.h>
#include <algorithm>

namespace dd {

// the command-line entry point
int dw(int argc, const char *const argv[]) {
  // available modes
  const std::map<std::string, int (*)(const CmdParser &)> MODES = {
      {"gibbs", gibbs},  // to do the learning and inference with Gibbs sampling
      {"text2bin", text2bin},  // to generate binary factor graphs from TSV
      {"bin2text", bin2text},  // to dump TSV of binary factor graphs
  };

  // parse command-line arguments
  CmdParser cmd_parser(argc, argv, MODES);
  if (cmd_parser.num_errors() > 0) return cmd_parser.num_errors();

  // dispatch to the correct function
  const auto &mode = MODES.find(cmd_parser.app_name);
  return (mode != MODES.end()) ? mode->second(cmd_parser) : 1;
}

int gibbs(const CmdParser &args) {
  // number of NUMA nodes
  size_t n_numa_node = NumaNodes::num_configured();
  // number of max threads per NUMA node
  size_t n_thread_per_numa = (sysconf(_SC_NPROCESSORS_CONF)) / (n_numa_node);

  FactorGraphDescriptor meta = read_meta(args.fg_file);

  // Allocate the input on the first group of NUMA nodes
  NumaNodes::partition(0, args.n_datacopy).bind();

  // Load factor graph
  FactorGraph *fg = new FactorGraph(meta);

  fg->load_variables(args.variable_file);
  fg->load_weights(args.weight_file);
  fg->load_domains(args.domain_file);
  fg->load_factors(args.factor_file);
  fg->safety_check();
  fg->construct_index();

  // Initialize Gibbs sampling application.
  DimmWitted dw(fg, fg->weights.get(), args);

  dw.learn();

  dw.dump_weights();

  dw.inference();

  if (dw.opts.n_inference_epoch > 0) {
    // dump only if we did any sampling at all
    dw.aggregate_results_and_dump();
  }

  return 0;
}

DimmWitted::DimmWitted(FactorGraph *p_cfg, const Weight weights[],
                       const CmdParser &opts)
    : n_samplers_(opts.n_datacopy), weights(weights), opts(opts) {
  size_t n_thread_per_numa =
      std::max(size_t(1), opts.n_threads / opts.n_datacopy);

  // copy factor graphs and create samplers
  size_t i = 0;
  for (auto &numa_nodes : NumaNodes::partition(opts.n_datacopy)) {
    numa_nodes.bind();
    std::cout << "CREATE CFG ON NODE ... " << numa_nodes << std::endl;
    samplers.push_back(GibbsSampler(
        std::unique_ptr<FactorGraph>(
            i == 0 ?
                   // use the given factor graph for the first sampler
                p_cfg
                   :
                   // then, make a copy for the rest，剩下的都是copy factor graph
                new FactorGraph(samplers[0].fg)),
        weights, numa_nodes, n_thread_per_numa, i, opts));
    ++i;
  }
}

void DimmWitted::inference() {
  const size_t n_epoch = compute_n_epochs(opts.n_inference_epoch);
  const size_t nvar = samplers[0].fg.size.num_variables;
  const bool should_show_progress = !opts.should_be_quiet;
  Timer t_total, t;

  for (auto &sampler : samplers) sampler.infrs.clear_variabletally();

  // inference epochs
  for (size_t i_epoch = 0; i_epoch < n_epoch; ++i_epoch) {
    if (should_show_progress) {
      std::streamsize ss = std::cout.precision();
      std::cout << std::setprecision(3) << "INFERENCE EPOCH "
                << i_epoch * n_samplers_ << "~"
                << ((i_epoch + 1) * n_samplers_ - 1) << "...." << std::flush
                << std::setprecision(ss);
    }

    // restart timer
    t.restart();

    // sample，相比学习过程，这里只做采样
    for (auto &sampler : samplers) sampler.sample(i_epoch);

    // wait for samplers to finish
    for (auto &sampler : samplers) sampler.wait();

    double elapsed = t.elapsed();
    if (should_show_progress) {
      std::streamsize ss = std::cout.precision();
      std::cout << std::setprecision(3) << "" << elapsed << " sec."
                << "," << (nvar * n_samplers_) / elapsed << " vars/sec"
                << std::endl
                << std::setprecision(ss);
    }
  }

  double elapsed = t_total.elapsed();
  std::cout << "TOTAL INFERENCE TIME: " << elapsed << " sec." << std::endl;
}

void DimmWitted::learn() {
  //第一个sampler保存最终的结果
  InferenceResult &infrs = samplers[0].infrs;

  const size_t n_epoch = compute_n_epochs(opts.n_learning_epoch);
  const size_t nweight = infrs.nweights;
  const double decay = opts.decay;
  const bool should_show_progress = !opts.should_be_quiet;
  Timer t_total, t;

  double current_stepsize = opts.stepsize;
  const std::unique_ptr<double[]> prev_weights(new double[nweight]);
  COPY_ARRAY_IF_POSSIBLE(infrs.weight_values.get(), nweight,
                         prev_weights.get());

  bool stop = false;

  // learning epochs
  for (size_t i_epoch = 0; !stop && i_epoch < n_epoch; ++i_epoch) {
    t.restart();

    // performs stochastic gradient descent with sampling
    for (auto &sampler : samplers) sampler.sample_sgd(current_stepsize);

    // wait the samplers to finish，线程等待
    for (auto &sampler : samplers) sampler.wait();

    stop = update_weights(infrs, t.elapsed(), current_stepsize, prev_weights);

    // assigned weights to all factor graphs
    for (size_t i = 1; i < n_samplers_; ++i)
      infrs.copy_weights_to(samplers[i].infrs);

    current_stepsize *= decay; //stepsize按照指定的衰退比例衰减
  }
}

//更新权重，多个sampler相加，取平均得到新的weight
bool DimmWitted::update_weights(InferenceResult &infrs,
                                double elapsed,
                                double stepsize,
                                const std::unique_ptr<double[]> &prev_weights) {
  // sum the weights and store in the first factor graph
  // the average weights will be calculated
  for (size_t i = 1; i < n_samplers_; ++i)
    //把其他sampler的权重都加到infrs上
    infrs.merge_weights_from(samplers[i].infrs);
  //权重求平均
  if (n_samplers_ > 1) infrs.average_weights(n_samplers_);

  // calculate the norms of the difference of weights from the current epoch
  // and last epoch，这一段代码很奇怪，计算了半天，经没有实际的外部影响
  double lmax = -INFINITY;
  double l2 = 0.0;
  for (size_t j = 0; j < infrs.nweights; ++j) {
    double diff = fabs(infrs.weight_values[j] - prev_weights[j]);
    l2 += diff * diff;
    
    if (lmax < diff) lmax = diff; //找到diff的最大值
  }
  lmax /= stepsize;

  // update prev_weights，将最新的weight赋值给pre_weights
  COPY_ARRAY(infrs.weight_values.get(), infrs.nweights, prev_weights.get());

  // TODO: early stopping based on convergence
  return false;
}

void DimmWitted::dump_weights() {
  // learning weights snippets
  const InferenceResult &infrs = samplers[0].infrs;

  if (!opts.should_be_quiet) infrs.show_weights_snippet(std::cout);

  // dump learned weights
  std::string filename_text(opts.output_folder +
                            "/inference_result.out.weights.text");
  std::cout << "DUMPING... TEXT    : " << filename_text << std::endl;
  std::ofstream fout_text(filename_text);
  infrs.dump_weights_in_text(fout_text);
  fout_text.close();
}

void DimmWitted::aggregate_results_and_dump() {
  InferenceResult &infrs = samplers[0].infrs;

  // aggregate assignments across all possible worlds
  for (size_t i = 1; i < n_samplers_; ++i)
    infrs.aggregate_marginals_from(samplers[i].infrs);

  if (!opts.should_be_quiet) infrs.show_marginal_snippet(std::cout);

  // dump inference results
  std::string filename_text(opts.output_folder + "/inference_result.out.text");
  std::ofstream fout_text(filename_text);
  infrs.dump_marginals_in_text(fout_text);
  fout_text.close();

  if (!opts.should_be_quiet) infrs.show_marginal_histogram(std::cout);
}

// compute number of NUMA-aware epochs for learning or inference
// 指定的epoch被分配给多个sampler
size_t DimmWitted::compute_n_epochs(size_t n_epoch) {
  return std::ceil((double)n_epoch / n_samplers_);
}

}  // namespace dd
