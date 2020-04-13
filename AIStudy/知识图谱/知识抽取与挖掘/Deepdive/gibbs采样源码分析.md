[TOC]

# Deepdive中dimmwitted模块Gibbs采样源码分析

## 1. 基础知识

### 1.1 NUMA

## 2. 代码分析

先理清核心类的定义，以此理解代码如何描述因子图。然后分析构建因子图的过程，训练和推理过程，以理解吉布斯采样部分的内容。

### 2.1 基础类

基础类包括以下类：

- FactorGraph: 描述因子图
- Factor: 描述单个因子
- Variable: 变量
- FactorToVariable: 描述因子到Variable的边
- Weight: 因子针对变量的权重
- VariableToFactor: 连接变量到因子的边

#### 2.1.1 FactorGraph

```c++
class FactorGraphDescriptor {
 public:
  FactorGraphDescriptor();

  FactorGraphDescriptor(size_t num_variables, size_t num_factors,
                        size_t num_weights, size_t num_edges);

  /** number of all variables */
  size_t num_variables;

  /** number of factors */
  size_t num_factors;

  /** number of edges */
  size_t num_edges;

  /** number of all weights */
  size_t num_weights;

  /** number of all values; populated in FactorGraph.construct_index */
  size_t num_values;

  /** number of evidence variables，证据变量？？，莫非指的是已确定取值的变量 */
  size_t num_variables_evidence;

  /** number of query variables，等待确定值得变量吗？ */
  size_t num_variables_query;
};

class FactorGraph {
 public:
  /** Capacity to allow multi-step loading，容量大小 */
  FactorGraphDescriptor capacity;

  /** Actual count of things，实际大小 */
  FactorGraphDescriptor size;

  // distinct weights
  std::unique_ptr<Weight[]> weights;

  // factors and each factor's variables (with "equal_to" values)
  std::unique_ptr<Factor[]> factors;
  std::unique_ptr<FactorToVariable[]> vifs;

  // variables, each variable's values, and index into factor IDs
  // factor_index follows sort order of adjacent <var, val>
  // |factor_index| may be smaller than |edges| because we deduplicate (see
  // construct_index)
  std::unique_ptr<Variable[]> variables;
  std::unique_ptr<size_t[]> factor_index;
  std::unique_ptr<VariableToFactor[]> values;

  void load_weights(const std::vector<std::string>& filenames);
  void load_variables(const std::vector<std::string>& filenames);
  void load_factors(const std::vector<std::string>& filenames);
  void load_domains(const std::vector<std::string>& filenames);

  // count data structures to ensure consistency with declared size
  void safety_check();
  // construct "values" and "factor_index" for var-to-factor lookups
  void construct_index();

  void construct_index_part(size_t v_start, size_t v_end, size_t val_base,
                            size_t fac_base);

  inline size_t get_var_value_at(const Variable& var, size_t idx) const {
    return values[var.var_val_base + idx].value;
  }

  inline const FactorToVariable& get_factor_vif_at(const Factor& factor,
                                                   size_t idx) const {
    return vifs[factor.vif_base + idx];
  }

  /**
   * Constructs a new factor graph with given number number of variables,
   * factors, weights, and edges
   */
  FactorGraph(const FactorGraphDescriptor& capacity);

  // copy constructor
  FactorGraph(const FactorGraph& other);

  ~FactorGraph();

  /**
   * Given a variable, updates the weights associated with the factors that
   * connect to the variable.
   * Used in learning phase, after sampling one variable,
   * update corresponding weights (stochastic gradient descent).
   */
  void sgd_on_variable(const Variable& variable, InferenceResult& infrs,
                       double stepsize, bool is_noise_aware);

  // perform SGD step for weight learning on one factor
  inline void sgd_on_factor(size_t factor_id, double stepsize, size_t vid,
                            size_t evidence_value, InferenceResult& infrs);

  /**
   * Returns log-linear weighted potential of the all factors for the given
   * variable using the propsal value.
   */
  inline double potential(const Variable& variable, const size_t proposal,
                          const size_t assignments[],
                          const double weight_values[]);
};
```

#### 2.1.2 Factor

```c++
typedef enum {
  FUNC_IMPLY_NATURAL = 0,
  FUNC_OR = 1,
  FUNC_AND = 2,
  FUNC_EQUAL = 3,
  FUNC_ISTRUE = 4,
  FUNC_LINEAR = 7,
  FUNC_RATIO = 8,
  FUNC_LOGICAL = 9,
  FUNC_AND_CATEGORICAL = 12,
  FUNC_IMPLY_MLN = 13,

  FUNC_UNDEFINED = -1,
} FACTOR_FUNCTION_TYPE;

/**
 * 便是因子图中的一个因子
 */
class Factor {
 public:
  size_t id;                     // factor id
  double feature_value;          // feature value
  size_t weight_id;              // weight id
  FACTOR_FUNCTION_TYPE func_id;  // factor function id，说明因子函数的类型
  size_t num_vars;               // number of variables
  size_t vif_base;               // start variable id in FactorGraph.vifs，在FactorGraph.vifs数组中的起始位置

  static constexpr size_t INVALID_ID = -1;

  /**
   * Turns out the no-arg constructor is still required, since we're
   * initializing arrays of these objects inside FactorGraph and
   * FactorGraph.
   */
  Factor();

  Factor(size_t id, double value, size_t weight_id,
         FACTOR_FUNCTION_TYPE func_id, size_t num_vars);

  Factor(const Factor &other);

  Factor &operator=(const Factor &other);

  inline bool is_categorical() const { return func_id == FUNC_AND_CATEGORICAL; }

#define POTENTIAL_SIGN(func_id) _potential_sign_##func_id

  /**
   * Returns potential of the factor.
   * (potential is the value of the factor)
   * The potential is calculated using the proposal value for variable with
   * id vid, and assignments for other variables in the factor.
   *
   * vifs pointer to variables in the factor graph
   * assignments pointer to variable values (array)
   * vid variable id to be calculated with proposal
   * proposal the proposed value.
   */
  inline double potential(
      const FactorToVariable vifs[], const size_t assignments[],
      const size_t vid = Variable::INVALID_ID,
      const size_t proposal = Variable::INVALID_VALUE) const {

#define RETURN_POTENTIAL_FOR(func_id)                                  \
  case func_id:                                                        \
    return POTENTIAL_SIGN(func_id)(vifs, assignments, vid, proposal) * this->feature_value

#define RETURN_POTENTIAL_FOR2(func_id, func_id2) \
  case func_id2:                                 \
    RETURN_POTENTIAL_FOR(func_id)
    switch (func_id) {
      RETURN_POTENTIAL_FOR(FUNC_IMPLY_MLN);
      RETURN_POTENTIAL_FOR(FUNC_IMPLY_NATURAL);
      RETURN_POTENTIAL_FOR2(FUNC_AND, FUNC_ISTRUE);
      RETURN_POTENTIAL_FOR(FUNC_OR);
      RETURN_POTENTIAL_FOR(FUNC_EQUAL);
      RETURN_POTENTIAL_FOR(FUNC_AND_CATEGORICAL);
      RETURN_POTENTIAL_FOR(FUNC_LINEAR);
      RETURN_POTENTIAL_FOR(FUNC_RATIO);
      RETURN_POTENTIAL_FOR(FUNC_LOGICAL);
#undef RETURN_POTENTIAL_FOR
      default:
        std::cout << "Unsupported FACTOR_FUNCTION_TYPE = " << func_id
                  << std::endl;
        std::abort();
    }
  }

 private:
  FRIEND_TEST(FactorTest, ONE_VAR_FACTORS);
  FRIEND_TEST(FactorTest, TWO_VAR_FACTORS);
  FRIEND_TEST(FactorTest, THREE_VAR_IMPLY);

  // whether a variable's value or proposal satisfies the is_equal condition
  inline bool is_variable_satisfied(const FactorToVariable &vif,
                                    const size_t &vid,
                                    const size_t assignments[],
                                    const size_t &proposal) const {
    return (vif.vid == vid) ? vif.satisfiedUsing(proposal)
                            : vif.satisfiedUsing(assignments[vif.vid]);
  }

//下面定义的就是不同的因子函数类型返回不同的值
#define DEFINE_POTENTIAL_SIGN_FOR(func_id)                       \
  inline double POTENTIAL_SIGN(func_id)(                         \
      const FactorToVariable vifs[], const size_t assignments[], \
      const size_t vid, const size_t &proposal) const

  /** Return the value of the "equality test" of the variables in the factor,
   * with the variable of index vid (wrt the factor) is set to the value of
   * the 'proposal' argument.
   *
   */
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_EQUAL) {
    const FactorToVariable &vif = vifs[vif_base];
    /* We use the value of the first variable in the factor as the "gold"
     * standard" */
    const bool firstsat =
        is_variable_satisfied(vif, vid, assignments, proposal);

    /* Iterate over the factor variables */
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      const bool satisfied =
          is_variable_satisfied(vif, vid, assignments, proposal);
      /* Early return as soon as we find a mismatch */
      if (satisfied != firstsat) return -1;
    }
    return 1;
  }

  /** Return the value of the logical AND of the variables in the factor, with
   * the variable of index vid (wrt the factor) is set to the value of the
   * 'proposal' argument.
   *
   */
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_AND) {
    /* Iterate over the factor variables */
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      const bool satisfied =
          is_variable_satisfied(vif, vid, assignments, proposal);
      /* Early return as soon as we find a variable that is not satisfied */
      if (!satisfied) return -1;
    }
    return 1;
  }

  // potential for AND factor over categorical variables
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_AND_CATEGORICAL) {
    /* Iterate over the factor variables */
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      const bool satisfied =
          is_variable_satisfied(vif, vid, assignments, proposal);
      /* Early return as soon as we find a variable that is not satisfied */
      if (!satisfied) return 0;
    }
    return 1;
  }

  /** Return the value of the logical OR of the variables in the factor, with
   * the variable of index vid (wrt the factor) is set to the value of the
   * 'proposal' argument.
   *
   */
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_OR) {
    /* Iterate over the factor variables */
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      const bool satisfied =
          is_variable_satisfied(vif, vid, assignments, proposal);
      /* Early return as soon as we find a variable that is satisfied */
      if (satisfied) return 1;
    }
    return -1;
  }

  /** Return the value of the 'imply (MLN version)' of the variables in the
   * factor, with the variable of index vid (wrt the factor) is set to the
   * value of the 'proposal' argument.
   *
   * The head of the 'imply' rule is stored as the *last* variable in the
   * factor.
   *
   * The truth table of the 'imply (MLN version)' function requires to return
   * 0.0 if the body of the imply is satisfied but the head is not, and to
   * return 1.0 if the body is not satisfied.
   *
   */
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_IMPLY_MLN) {
    /* Compute the value of the body of the rule */
    bool bBody = true;
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars - 1; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      // If it is the proposal variable, we use the truth value of the proposal
      bBody &= is_variable_satisfied(vif, vid, assignments, proposal);
    }

    if (!bBody) {
      // Early return if the body is not satisfied
      return 1;
    } else {
      // Compute the value of the head of the rule
      const FactorToVariable &vif =
          vifs[vif_base + num_vars - 1];  // encoding of the head, should
                                          // be more structured.
      const bool bHead = is_variable_satisfied(vif, vid, assignments, proposal);
      return bHead ? 1 : 0;
    }
  }

  /** Return the value of the 'imply' of the variables in the factor, with the
   * variable of index vid (wrt the factor) is set to the value of the
   * 'proposal' argument.
   *
   * The head of the 'imply' rule is stored as the *last* variable in the
   * factor.
   *
   * The truth table of the 'imply' function requires to return
   * -1.0 if the body of the rule is satisfied but the head is not, and to
   *  return 0.0 if the body is not satisfied.
   *
   */
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_IMPLY_NATURAL) {
    /* Compute the value of the body of the rule */
    bool bBody = true;
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars - 1; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      // If it is the proposal variable, we use the truth value of the proposal
      bBody &= is_variable_satisfied(vif, vid, assignments, proposal);
    }

    if (!bBody) {
      // Early return if the body is not satisfied
      return 0;
    } else {
      // Compute the value of the head of the rule */
      const FactorToVariable &vif =
          vifs[vif_base + num_vars - 1];  // encoding of the head, should
                                          // be more structured.
      bool bHead = is_variable_satisfied(vif, vid, assignments, proposal);
      return bHead ? 1 : -1;
    }
  }

  // potential for linear expression
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_LINEAR) {
    double res = 0.0;
    bool bHead = is_variable_satisfied(vifs[vif_base + num_vars - 1], vid,
                                       assignments, proposal);
    /* Compute the value of the body of the rule */
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars - 1; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      const bool satisfied =
          is_variable_satisfied(vif, vid, assignments, proposal);
      res += ((1 - satisfied) || bHead);
    }
    if (num_vars == 1)
      return double(bHead);
    else
      return res;
  }

  // potential for linear expression
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_RATIO) {
    double res = 1.0;
    bool bHead = is_variable_satisfied(vifs[vif_base + num_vars - 1], vid,
                                       assignments, proposal);
    /* Compute the value of the body of the rule */
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars - 1; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      const bool satisfied =
          is_variable_satisfied(vif, vid, assignments, proposal);
      res += ((1 - satisfied) || bHead);
    }
    if (num_vars == 1) return log2(res + double(bHead));
    return log2(res);
  }

  // potential for linear expression
  DEFINE_POTENTIAL_SIGN_FOR(FUNC_LOGICAL) {
    double res = 0.0;
    bool bHead = is_variable_satisfied(vifs[vif_base + num_vars - 1], vid,
                                       assignments, proposal);
    /* Compute the value of the body of the rule */
    for (size_t i_vif = vif_base; i_vif < vif_base + num_vars - 1; ++i_vif) {
      const FactorToVariable &vif = vifs[i_vif];
      const bool satisfied =
          is_variable_satisfied(vif, vid, assignments, proposal);
      res += ((1 - satisfied) || bHead);
    }
    if (num_vars == 1)
      return double(bHead);
    else {
      if (res > 0.0)
        return 1.0;
      else
        return 0.0;
    }
  }

#undef DEFINE_POTENTIAL_SIGN_FOR
};
```

#### 2.1.3 FactorToVariable & VariableToFactor

```c++
class VariableToFactor {
 public:
  // original (sparse) value as assigned by DD grounding
  size_t value;
  // soft evidence weight. range: [0, 1].
  // NOTE: for categorical only
  double truthiness;
  // base offset into the factor index (FactorGraph.factor_index)
  size_t factor_index_base;
  // number of entries in the factor index
  size_t factor_index_length;

  VariableToFactor() : VariableToFactor(Variable::INVALID_ID, 0, -1, 0) {}

  VariableToFactor(size_t v, double t, size_t base, size_t len)
      : value(v),
        truthiness(t),
        factor_index_base(base),
        factor_index_length(len) {}
};

/**
 * Encapsulates a variable inside a factor
 */
class FactorToVariable {
 public:
  size_t vid;  // variable id
  // dense-form value binding to the var in the factor
  // - Boolean: {0, 1} depending on wheter atom is negated in rule head
  // - Categorical: [0..cardinality) depending on the var relation tuple
  size_t dense_equal_to;

  /**
   * Returns whether the variable's predicate is satisfied using the given
   * value.
   * Applies to both boolean and categorical.
   */
  inline bool satisfiedUsing(size_t dense_value) const {
    return dense_equal_to == dense_value;
  }

  FactorToVariable();

  FactorToVariable(size_t vid, size_t dense_equal_to);
};
```

#### 2.1.4 Variable

```c++

typedef enum {
  DTYPE_BOOLEAN = 0,
  DTYPE_CATEGORICAL = 1,
} DOMAIN_TYPE;

// Used to store back refs to factors in a Variable at loading time.
// Deallocated in FactorGraph.construct_index.
class TempValueFactor {
 public:
  size_t value_dense;
  size_t factor_id;

  TempValueFactor(size_t value_dense_in, size_t factor_id_in)
      : value_dense(value_dense_in), factor_id(factor_id_in){};

  // Lexical sort order for indexing
  bool operator<(const TempValueFactor& other) const {
    return value_dense < other.value_dense ||
           (value_dense == other.value_dense && factor_id < other.factor_id);
  }
};

// Used as value in Variable.domain_map
typedef struct {
  size_t index;
  double truthiness;
} TempVarValue;

/**
 * A variable in the factor graph.
 */
class Variable {
 public:
  // While a categorical var has `cardinality` VariableToFactor objects,
  // a boolean var only has one VariableToFactor object in FactorGraph.values
  // and one entry in InferenceResult.sample_tallies.
  // BOOLEAN_DENSE_VALUE is used to index into those arrays.
  static constexpr size_t BOOLEAN_DENSE_VALUE = 0;
  static constexpr size_t INVALID_ID = (size_t)-1;
  static constexpr size_t INVALID_VALUE = (size_t)-1;

  size_t id;                // variable id
  DOMAIN_TYPE domain_type;  // can be DTYPE_BOOLEAN or DTYPE_CATEGORICAL，布尔值或分类值
  bool is_evid;             // whether the variable is evidence
  size_t cardinality;       // cardinality; 2 for boolean

  // After loading (Factorgraph.construct_index), all assignment values
  // and all proposal values take the "dense" form: 稠密的形式
  // - Boolean: {0, 1}
  // - Categorical: [0..cardinality)
  size_t assignment_dense;

  // Sum of all values' truthiness
  double total_truthiness;

  // We concatenate the list of "possible values" for each variable to form
  // FactorGraph.values (also InferenceResults.sample_tallies).
  // - For boolean, there is just one value, namely BOOLEAN_DENSE_VALUE
  // - For categorical, there are `cardinality` values
  //   - if domain is specified, it's the sorted list of domain values
  //   - otherwise, it's [0..cardinality)
  //
  // var_val_base is the start position into those lists.
  size_t var_val_base;

  // Map from value to index in the domain vector.
  // Populated at load time (FactorGraph.load_domains).
  // Deallocated in FactorGraph.construct_index.
  std::unique_ptr<std::unordered_map<size_t, TempVarValue>> domain_map;

  // Backrefs to factors (including factor's "equal_to" value).
  // Populated at load time (FactorGraph.load_factors). 加载factor时生成
  // Deallocated in FactorGraph.construct_index.
  std::unique_ptr<std::vector<TempValueFactor>>
      adjacent_factors;  // factor ids the variable connects to，与变量相邻的factor

  Variable();  // default constructor, necessary for
               // FactorGraph::variables

  Variable(size_t id, DOMAIN_TYPE domain_type, bool is_evidence,
           size_t cardinality, size_t init_value);

  /**
   * Constructs a variable with only the important information from a
   * temporary variable
   */
  Variable(const Variable& variable);
  Variable& operator=(const Variable& variable);

  inline void add_value_factor(size_t value_dense, size_t factor_id) {
    if (!adjacent_factors) {
      adjacent_factors.reset(new std::vector<TempValueFactor>());
    }
    adjacent_factors->push_back(TempValueFactor(value_dense, factor_id));
  }

  inline bool is_boolean() const { return domain_type == DTYPE_BOOLEAN; }

  inline bool has_truthiness() const {
    return !is_linear_zero(total_truthiness);
  }

  inline size_t internal_cardinality() const {
    return is_boolean() ? 1 : cardinality;
  }

  inline size_t var_value_offset(size_t value_dense) const {
    return is_boolean() ? BOOLEAN_DENSE_VALUE : value_dense;
  }

  // get the index of the value
  inline size_t get_domain_index(size_t v) const {
    return domain_map ? domain_map->at(v).index : v;
  }
};
```

#### 2.1.5 Weight

```c++
/**
 * Encapsulates a weight for factors.
 */
class Weight {
 public:
  size_t id;      // weight id，这里的ID在哪里使用呢？在factor graph中，weight是数组，莫非是和因子数组索引相对应
  double weight;  // weight value
  bool isfixed;   // whether the weight is fixed

  Weight(size_t id, double weight, bool isfixed);

  Weight();

  static constexpr size_t INVALID_ID = (size_t)-1;
};
```

#### 2.1.6

```c++

```

### 2.2 因子图构建过程

因子图的构建其实就是加载数据的过程，加载variable、weights、domains、factors，加载完成之后进行safety_check和construct_index。

1. 加载meta数据

meta数据存于一个meta文件中，按照代码的逻辑，里面关键的内容是与因子图有关的权重、变量、因子、边的数量。加载代码如下：

```c++
FactorGraphDescriptor read_meta(const std::string &meta_file) {
  FactorGraphDescriptor meta;
  std::ifstream file(meta_file);
  std::string buf;
  
  getline(file, buf, ','); //从输入流中读取字符串，第三个参数是分隔符
  meta.num_weights = atoll(buf.c_str());
  
  getline(file, buf, ',');
  meta.num_variables = atoll(buf.c_str());
  
  getline(file, buf, ',');
  meta.num_factors = atoll(buf.c_str());
  
  getline(file, buf, ',');
  meta.num_edges = atoll(buf.c_str());
  
  return meta;
}
```

2. 加载变量

并发从variable文件中加载变量数据。

```c++

//并发加载函数
inline void parallel_load(
    const std::vector<std::string> &filenames,
    std::function<void(const std::string &filename)> loader) {
  std::vector<std::thread> threads;
  for (const auto &filename : filenames)
    threads.push_back(std::thread(loader, filename));
  for (auto &t : threads) t.join();
  threads.clear();
}

//加载变量，并发是根据变量的文件并发的，一个文件一个线程
void FactorGraph::load_variables(const std::vector<std::string> &filenames) {
  std::mutex mtx;

  parallel_load(filenames, [this, &mtx](const std::string &filename) {
    std::ifstream file(filename, std::ios::binary);
    size_t num_variables = 0;
    size_t num_variables_evidence = 0;
    size_t num_variables_query = 0;
    while (file && file.peek() != EOF) {
      size_t vid;
      uint8_t role_serialized;
      size_t initial_value;
      uint16_t dtype_serialized;
      size_t cardinality;
      // read fields
      read_be_or_die(file, vid); //根据第二个参数的类型，读取相应数量的字节，然后进行类型转换
      read_be_or_die(file, role_serialized);
      read_be_or_die(file, initial_value);
      read_be_or_die(file, dtype_serialized);
      read_be_or_die(file, cardinality); //deepdive中的默认是2，也就是说是变量是bool类型
      // map serialized to internal values
      DOMAIN_TYPE dtype;
      switch (dtype_serialized) {
        case 0: //dtype_serialized在deepdive中的默认值是0，因为里面的变量是true、false
          dtype = DTYPE_BOOLEAN;
          break;
        case 1:
          dtype = DTYPE_CATEGORICAL;
          break;
        default:
          std::cerr << "[ERROR] Only Boolean and Categorical "
                       "variables are supported "
                       "now!"
                    << std::endl;
          std::abort();
      }

      //这个变量是否是确定的事实，大于等于1，就是，bool变量的true，其实就是
      bool is_evidence = role_serialized >= 1;

      size_t init_value = is_evidence ? initial_value : 0;
      variables[vid] =
          Variable(vid, dtype, is_evidence, cardinality, init_value);
      ++num_variables;
      if (is_evidence) {
        ++num_variables_evidence;
      } else {
        ++num_variables_query;
      }
    }
    {  // commit counts
      std::lock_guard<std::mutex> lck(mtx);
      size.num_variables += num_variables;
      size.num_variables_evidence += num_variables_evidence;
      size.num_variables_query += num_variables_query;
    }
  });
}

```

3. 加载因子权重

并发从权重文件中加载因子权重信息。

```c++
void FactorGraph::load_weights(const std::vector<std::string> &filenames) {
  std::mutex mtx;
  parallel_load(filenames, [this, &mtx](const std::string &filename) {
    std::ifstream file(filename, std::ios::binary);
    size_t count = 0;
    while (file && file.peek() != EOF) {
      // read fields
      size_t wid;
      uint8_t isfixed;
      double initial_value;
      read_be_or_die(file, wid);
      read_be_or_die(file, isfixed);
      read_be_or_die(file, initial_value);
      // load into factor graph
      weights[wid] = Weight(wid, initial_value, isfixed);
      ++count;
    }
    {  // commit counts
      std::lock_guard<std::mutex> lck(mtx);
      size.num_weights += count;
    }
  });
}
```

4. 加载因子信息

```c++
void FactorGraph::load_factors(const std::vector<std::string> &filenames) {
  std::mutex mtx;
  // an array of mutexes for serializing accesses to the variables
  std::unique_ptr<std::mutex[]> mtx_variables(
      new std::mutex[size.num_variables]);
  std::atomic<size_t> factor_cntr(0), edge_cntr(0);
  parallel_load(filenames, [this, &mtx, &mtx_variables, &factor_cntr,
                            &edge_cntr](const std::string &filename) {
    std::ifstream file(filename, std::ios::binary);
    size_t num_factors = 0;
    size_t num_edges = 0;
    while (file && file.peek() != EOF) {
      uint16_t type;
      size_t arity;
      // read fields
      read_be_or_die(file, type);
      read_be_or_die(file, arity);
      // register the factor，原子增加1，获取factor的id
      size_t idx = factor_cntr.fetch_add(1, std::memory_order_relaxed);
      ++num_factors;
      factors[idx] = Factor(idx, DEFAULT_FEATURE_VALUE, Weight::INVALID_ID,
                            (FACTOR_FUNCTION_TYPE)type, arity);

      size_t edge_idx = edge_cntr.fetch_add(arity, std::memory_order_relaxed);
      num_edges += arity;
      factors[idx].vif_base = edge_idx; //与factor相连的变量变量所在数组的起始位置
      for (size_t position = 0; position < arity; ++position) { //通过这里我们可以知道，factor文件中会连续存储多个关于相关变量的信息
        // read fields for each variable reference
        size_t variable_id;
        size_t should_equal_to;
        read_be_or_die(file, variable_id);
        read_be_or_die(file, should_equal_to);
        assert(variable_id < capacity.num_variables && variable_id >= 0);
        // convert original var value into dense value
        size_t dense_val =
            variables[variable_id].get_domain_index(should_equal_to);
        vifs[edge_idx] = FactorToVariable(variable_id, dense_val); //这里存放的是与factor有关的变量
        // add to adjacency lists
        if (variables[variable_id].is_boolean()) {
          // normalize boolean var vals to 0 for indexing purpusoes
          dense_val = Variable::BOOLEAN_DENSE_VALUE;
        }
        {
          std::lock_guard<std::mutex> lck(mtx_variables[variable_id]);
          variables[variable_id].add_value_factor(dense_val, idx); //将factor的id添加到Variable
        }
        ++edge_idx;
      }

      size_t wid;
      read_be_or_die(file, wid); //一个factor只有一个weight，但是却对应多个variable。
      factors[idx].weight_id = wid;
      double val;
      read_be_or_die(file, val);
      factors[idx].feature_value = val;
    }
    {  // commit counts
      std::lock_guard<std::mutex> lck(mtx);
      size.num_factors += num_factors;
      size.num_edges += num_edges;
    }
  });
}
```

5. safety check

检查因子图构建的是否正确。

```c++
void FactorGraph::safety_check() {
  // check if any space is wasted
  assert(capacity.num_variables == size.num_variables);
  assert(capacity.num_factors == size.num_factors);
  assert(capacity.num_edges == size.num_edges);
  assert(capacity.num_weights == size.num_weights);

  // check whether variables, factors, and weights are stored
  // in the order of their id
  for (size_t i = 0; i < size.num_variables; ++i) {
    assert(this->variables[i].id == i);
  }
  for (size_t i = 0; i < size.num_factors; ++i) {
    assert(this->factors[i].id == i);
  }
  for (size_t i = 0; i < size.num_weights; ++i) {
    assert(this->weights[i].id == i);
  }
}
```

6. construct index

```c++
// Construct index using multiple threads
// 6 sec instead of 30 sec for a 270M-factor graph
// std::vector<std::tuple<size_t, size_t, size_t, size_t>> params;
void FactorGraph::construct_index() {
  size_t total = size.num_variables;
  size_t cores = sysconf(_SC_NPROCESSORS_CONF);
  size_t increment = total / cores;

  // small graph, single thread
  if (total < 1000) {
    increment = total;
  }

  size_t milestone = 0;
  size_t num_values = 0, num_factors = 0;

  std::vector<std::function<void()>> tasks;
  for (size_t i = 0; i < size.num_variables; ++i) {
    if (i == milestone) {
      milestone += increment;
      if (milestone > total) {
        milestone = total;
      }
      tasks.push_back([this, i, milestone, num_values, num_factors]() {
        construct_index_part(i, milestone, num_values, num_factors);
      });
    }
    num_values += variables[i].internal_cardinality();
    if (variables[i].adjacent_factors) {
      num_factors += variables[i].adjacent_factors->size();
    }
  }

  size.num_values = capacity.num_values = num_values;
  values.reset(fast_alloc_no_init<VariableToFactor>(num_values));

  std::vector<std::thread> threads;
  for (const auto &task : tasks) {
    threads.push_back(std::thread(task));
  }
  for (auto &t : threads) t.join();
  threads.clear();
}

void FactorGraph::construct_index_part(size_t v_start, size_t v_end,
                                       size_t val_base, size_t fac_base) {
  size_t value_index_base = val_base, factor_index_base = fac_base;

  std::vector<size_t> value_list;
  std::vector<double> truthiness_list;

  // For each variable, sort and uniq adjacent factors by value. //排序和去重
  // We deallocate "domain_map" and "adjacent_factors".
  for (size_t i = v_start; i < v_end; ++i) {
    Variable &v = variables[i];
    v.var_val_base = value_index_base;
    v.total_truthiness = 0;

    if (v.is_boolean()) {
      // NOTE: we don't support truthiness for boolean vars
      values[value_index_base] =
          VariableToFactor(Variable::BOOLEAN_DENSE_VALUE, 0, 0, 0);
      ++value_index_base;
    } else {
      if (v.domain_map) {
        // explicitly listed domain values; recover the list from map.
        value_list.assign(v.cardinality, Variable::INVALID_VALUE);
        truthiness_list.assign(v.cardinality, 0);
        for (const auto &item : *v.domain_map) {
          value_list.at(item.second.index) = item.first;
          truthiness_list.at(item.second.index) = item.second.truthiness;
          v.total_truthiness += item.second.truthiness;
        }
        for (size_t j = 0; j < v.cardinality; ++j) {
          // catch spurious values (e.g., due to duplicate tuples from DD)
          assert(value_list[j] != Variable::INVALID_VALUE);
          values[value_index_base] =
              VariableToFactor(value_list[j], truthiness_list[j], 0, 0);
          ++value_index_base;
        }
        v.domain_map.reset();  // reclaim memory
      } else {
        // implicit [0...(cardinality-1)] domain values
        // TODO: this branch should be deprecated; i.e., require domains for all
        // categorical vars
        for (size_t j = 0; j < v.cardinality; ++j) {
          values[value_index_base] = VariableToFactor(j, 0, 0, 0);
          ++value_index_base;
        }
      }
    }

    if (v.adjacent_factors) {
      // sort by <value, fid>
      std::sort(v.adjacent_factors->begin(), v.adjacent_factors->end());
      size_t value_dense = Variable::INVALID_VALUE;
      size_t last_factor_id = Factor::INVALID_ID;
      for (const auto &item : *v.adjacent_factors) {
        if (item.value_dense != value_dense) {
          value_dense = item.value_dense;
          assert(value_dense < v.cardinality);
          values[v.var_val_base + value_dense].factor_index_base =
              factor_index_base;
        } else if (item.factor_id == last_factor_id) {
          continue;  // dedupe
        }
        factor_index[factor_index_base] = item.factor_id;
        ++factor_index_base;
        ++values[v.var_val_base + value_dense].factor_index_length;
        last_factor_id = item.factor_id;
      }
      v.adjacent_factors.reset();  // reclaim memory
    }
  }
}
```

### 2.3 吉布斯采样

#### 2.3.1 采样有关的类

1. DimmWitted类

```c++
/**
 * Class for (NUMA-aware) gibbs sampling
 *
 * This class encapsulates gibbs learning and inference, and dumping results.
 * Note the factor graph is copied on each NUMA node.
 * 这个类封装了推理、学习、导出权重的方法，每个Numa Node有一个factor graph的copy。
 */
class DimmWitted {
 private:
  const size_t n_samplers_;

 public:
  const Weight* const weights;  // TODO clarify ownership

  // command line parser
  const CmdParser& opts;  // TODO clarify ownership

  // factor graph copies per NUMA node
  std::vector<GibbsSampler> samplers;

  /**
   * Constructs DimmWitted class with given factor graph, command line
   * parser,
   * and number of data copies. Allocate factor graph to NUMA nodes.
   * n_datacopy number of factor graph copies. n_datacopy = 1 means only
   * keeping one factor graph.
   */
  DimmWitted(FactorGraph* p_cfg, const Weight weights[], const CmdParser& opts);

  /**
   * Performs learning
   * n_epoch number of epochs. A epoch is one pass over data
   * n_sample_per_epoch not used any more.
   * stepsize starting step size for weight update (aka learning rate)
   * decay after each epoch, the stepsize is updated as stepsize = stepsize *
   * decay
   * reg_param regularization parameter
   * is_quiet whether to compress information display
   */
  void learn();

  /**
   * Performs inference
   * n_epoch number of epochs. A epoch is one pass over data
   * is_quiet whether to compress information display
   */
  void inference();

  /**
   * Aggregates results from different NUMA nodes
   * Dumps the inference result for variables
   * is_quiet whether to compress information display
   */
  void aggregate_results_and_dump();

  /**
   * Dumps the learned weights
   * is_quiet whether to compress information display
   */
  void dump_weights();

 private:
  bool update_weights(InferenceResult& infrs, double elapsed, double stepsize,
                      const std::unique_ptr<double[]>& prev_weights);
  size_t compute_n_epochs(size_t n_epoch);
};
```

2. GibbsSampler 采样器

```c++
/**
 * Class for a single NUMA node sampler
 */
class GibbsSampler {
 private:
  std::unique_ptr<FactorGraph> pfg;
  std::unique_ptr<InferenceResult> pinfrs;
  NumaNodes numa_nodes_;
  std::vector<GibbsSamplerThread> workers;
  std::vector<std::thread> threads;

 public:
  FactorGraph &fg;
  InferenceResult &infrs; //推理结果

  // number of threads
  size_t nthread;
  // node id
  size_t nodeid;

  /**
   * Constructs a GibbsSampler given factor graph, number of threads, and
   * node id.
   */
  GibbsSampler(std::unique_ptr<FactorGraph> pfg, const Weight weights[],
               const NumaNodes &numa_nodes, size_t nthread, size_t nodeid,
               const CmdParser &opts);

  /**
   * Performs sample
   */
  void sample(size_t i_epoch);

  /**
   * Performs SGD
   */
  void sample_sgd(double stepsize);

  /**
   * Waits for sample worker to finish
   */
  void wait();
};

/**
 * Class for single thread sampler
 */
class GibbsSamplerThread {
 private:
  // shard and variable id range assigned to this one
  size_t start, end;

  // RNG seed
  unsigned short p_rand_seed[3];

  // potential for each proposals for categorical
  std::vector<double> varlen_potential_buffer_;

  // references and cached flags
  FactorGraph &fg;
  InferenceResult &infrs;
  bool sample_evidence;
  bool learn_non_evidence;
  bool is_noise_aware;

 public:
  /**
   * Constructs a GibbsSamplerThread with given factor graph
   */
  GibbsSamplerThread(FactorGraph &fg, InferenceResult &infrs, size_t i_sharding,
                     size_t n_sharding, const CmdParser &opts);

  /**
   * Samples variables. The variables are divided into n_sharding equal
   * partitions
   * based on their ids. This function samples variables in the i_sharding-th
   * partition.
   */
  void sample();

  /**
   * Performs SGD with by sampling variables.  The variables are divided into
   * n_sharding equal partitions based on their ids. This function samples
   * variables
   * in the i_sharding-th partition.
   */
  void sample_sgd(double stepsize);

  /**
   * Performs SGD by sampling a single variable with id vid
   */
  inline void sample_sgd_single_variable(size_t vid, double stepsize);

  /**
   * Samples a single variable with id vid
   */
  inline void sample_single_variable(size_t vid);

  // sample an "evidence" variable (parallel Gibbs conditioned on evidence)
  inline size_t sample_evid(const Variable &variable);

  // sample a single variable (regular Gibbs)
  inline size_t draw_sample(const Variable &variable,
                            const size_t assignments[],
                            const double weight_values[]);

  /**
    * Resets RNG seed to given values
    */
  void set_random_seed(unsigned short s0, unsigned short s1, unsigned short s2);
};

inline void GibbsSamplerThread::sample_sgd_single_variable(size_t vid,
                                                           double stepsize) {
  // stochastic gradient ascent
  // gradient of weight = E[f|D] - E[f], where D is evidence variables,
  // f is the factor function, E[] is expectation. Expectation is calculated
  // using a sample of the variable.

  const Variable &variable = fg.variables[vid];

  // pick a value for the regular Gibbs chain
  size_t proposal = draw_sample(variable, infrs.assignments_free.get(),
                                infrs.weight_values.get());
  infrs.assignments_free[variable.id] = proposal;

  // pick a value for the (parallel) evid Gibbs chain
  infrs.assignments_evid[variable.id] = sample_evid(variable);

  if (!learn_non_evidence && ((!is_noise_aware && !variable.is_evid) ||
                              (is_noise_aware && !variable.has_truthiness())))
    return;

  fg.sgd_on_variable(variable, infrs, stepsize, is_noise_aware);
}

inline void GibbsSamplerThread::sample_single_variable(size_t vid) {
  // this function uses the same sampling technique as in
  // sample_sgd_single_variable

  const Variable &variable = fg.variables[vid];

  if (!variable.is_evid || sample_evidence) {
    size_t proposal = draw_sample(variable, infrs.assignments_evid.get(),
                                  infrs.weight_values.get());
    infrs.assignments_evid[variable.id] = proposal;

    // bookkeep aggregates for computing marginals
    ++infrs.agg_nsamples[variable.id];
    if (!variable.is_boolean() || proposal == 1) {
      ++infrs.sample_tallies[variable.var_val_base +
                             variable.var_value_offset(proposal)];
    }
  }
}

inline size_t GibbsSamplerThread::sample_evid(const Variable &variable) {
  if (!is_noise_aware && variable.is_evid) {
    // direct assignment of hard "evidence"
    return variable.assignment_dense;
  } else if (is_noise_aware && variable.has_truthiness()) {
    // truthiness-weighted sample of soft "evidence" values
    double r = erand48(p_rand_seed);
    double sum = 0;
    for (size_t i = 0; i < variable.cardinality; ++i) {
      double truthiness = fg.values[variable.var_val_base + i].truthiness;
      sum += truthiness;
      if (sum >= r) return i;
    }
    return 0;
  } else {
    // Gibbs sample on the assignments_evid chain
    return draw_sample(variable, infrs.assignments_evid.get(),
                       infrs.weight_values.get());
  }
}

inline size_t GibbsSamplerThread::draw_sample(const Variable &variable,
                                              const size_t assignments[],
                                              const double weight_values[]) {
  size_t proposal = 0;

  switch (variable.domain_type) {
    case DTYPE_BOOLEAN: {
      double potential_pos;
      double potential_neg;
      potential_pos = fg.potential(variable, 1, assignments, weight_values);
      potential_neg = fg.potential(variable, 0, assignments, weight_values);

      double r = erand48(p_rand_seed);
      // sample the variable
      // flip a coin with probability
      // (exp(potential_pos) + exp(potential_neg)) / exp(potential_neg)
      // = exp(potential_pos - potential_neg) + 1
      if (r * (1.0 + exp(potential_neg - potential_pos)) < 1.0) {
        proposal = 1;
      } else {
        proposal = 0;
      }
      break;
    }

    case DTYPE_CATEGORICAL: {
      varlen_potential_buffer_.reserve(variable.cardinality);
      double sum = -100000.0;
      proposal = Variable::INVALID_VALUE;
// calculate potential for each proposal given a way to iterate the domain
#define COMPUTE_PROPOSAL(EACH_DOMAIN_VALUE, DOMAIN_VALUE, DOMAIN_INDEX)       \
  do {                                                                        \
          for                                                                 \
      EACH_DOMAIN_VALUE {                                                     \
        varlen_potential_buffer_[DOMAIN_INDEX] =                              \
            fg.potential(variable, DOMAIN_VALUE, assignments, weight_values); \
        sum = logadd(sum, varlen_potential_buffer_[DOMAIN_INDEX]);            \
      }                                                                       \
    double r = erand48(p_rand_seed);                                          \
        for                                                                   \
      EACH_DOMAIN_VALUE {                                                     \
        r -= exp(varlen_potential_buffer_[DOMAIN_INDEX] - sum);               \
        if (r <= 0) {                                                         \
          proposal = DOMAIN_VALUE;                                            \
          break;                                                              \
        }                                                                     \
      }                                                                       \
  } while (0)
      // All sparse values have been converted into dense values in
      // FactorGraph.load_domains
      COMPUTE_PROPOSAL((size_t i = 0; i < variable.cardinality; ++i), i, i);

      assert(proposal != Variable::INVALID_VALUE);
      break;
    }

    default:
      // unsupported variable types
      std::abort();
  }

  return proposal;
}
```

#### 2.3.2 吉布斯采样learn过程

1. learn方法的入口函数

```c++
void DimmWitted::learn() {
  InferenceResult &infrs = samplers[0].infrs;

  const size_t n_epoch = compute_n_epochs(opts.n_learning_epoch);
  const size_t nweight = infrs.nweights;
  const double decay = opts.decay; //衰退比例
  const bool should_show_progress = !opts.should_be_quiet;
  Timer t_total, t;

  double current_stepsize = opts.stepsize;
  //保存之前的权重信息
  const std::unique_ptr<double[]> prev_weights(new double[nweight]);
  COPY_ARRAY_IF_POSSIBLE(infrs.weight_values.get(), nweight,
                         prev_weights.get());

  bool stop = false;

  // learning epochs
  for (size_t i_epoch = 0; !stop && i_epoch < n_epoch; ++i_epoch) {
    //打印过程信息
    if (should_show_progress) {
      std::streamsize ss = std::cout.precision();
      std::cout << std::setprecision(3) << "LEARNING EPOCH "
                << i_epoch * n_samplers_ << "~"
                << ((i_epoch + 1) * n_samplers_ - 1) << "...." << std::flush
                << std::setprecision(ss);
    }

    t.restart(); //定时器开始

    // performs stochastic gradient descent with sampling，随机梯度下降
    for (auto &sampler : samplers) sampler.sample_sgd(current_stepsize);

    // wait the samplers to finish
    for (auto &sampler : samplers) sampler.wait();

    //这里的更新逻辑是需要关注的，不同的线程单独训练，然后更新同一个pre_weights
    stop = update_weights(infrs, t.elapsed(), current_stepsize, prev_weights);

    // assigned weights to all factor graphs
    for (size_t i = 1; i < n_samplers_; ++i)
      infrs.copy_weights_to(samplers[i].infrs);

    current_stepsize *= decay; //步长按照decay指定的比例衰退
  }

  double elapsed = t_total.elapsed();
  std::cout << "TOTAL LEARNING TIME: " << elapsed << " sec." << std::endl;
}
```

2. sample_sgd 基于随机梯度下降的采样学习

```c++
void GibbsSampler::sample_sgd(double stepsize) {
  numa_nodes_.bind();
  for (auto &worker : workers) {
    threads.push_back(
        //调用GibbsSamplerThread.sample_sgd
        std::thread([&worker, stepsize]() { worker.sample_sgd(stepsize); }));
  }
}
```

```c++
void GibbsSamplerThread::sample_sgd(double stepsize) {
  for (size_t vid = start; vid < end; ++vid) {
    sample_sgd_single_variable(vid, stepsize);
  }
}
```

```c++
inline void GibbsSamplerThread::sample_sgd_single_variable(size_t vid,
                                                           double stepsize) {
  // stochastic gradient ascent
  // gradient of weight = E[f|D] - E[f], where D is evidence variables,
  // f is the factor function, E[] is expectation. Expectation is calculated
  // using a sample of the variable.

  const Variable &variable = fg.variables[vid];

  // pick a value for the regular Gibbs chain
  size_t proposal = draw_sample(variable, infrs.assignments_free.get(),
                                infrs.weight_values.get());
  infrs.assignments_free[variable.id] = proposal;

  // pick a value for the (parallel) evid Gibbs chain
  infrs.assignments_evid[variable.id] = sample_evid(variable);

  if (!learn_non_evidence && ((!is_noise_aware && !variable.is_evid) ||
                              (is_noise_aware && !variable.has_truthiness())))
    return;

  fg.sgd_on_variable(variable, infrs, stepsize, is_noise_aware);
}

inline size_t GibbsSamplerThread::sample_evid(const Variable &variable) {
  if (!is_noise_aware && variable.is_evid) {
    // direct assignment of hard "evidence"
    return variable.assignment_dense;
  } else if (is_noise_aware && variable.has_truthiness()) {
    // truthiness-weighted sample of soft "evidence" values
    double r = erand48(p_rand_seed);
    double sum = 0;
    for (size_t i = 0; i < variable.cardinality; ++i) {
      double truthiness = fg.values[variable.var_val_base + i].truthiness;
      sum += truthiness;
      if (sum >= r) return i;
    }
    return 0;
  } else {
    // Gibbs sample on the assignments_evid chain
    return draw_sample(variable, infrs.assignments_evid.get(),
                       infrs.weight_values.get());
  }
}

inline size_t GibbsSamplerThread::draw_sample(const Variable &variable,
                                              const size_t assignments[],
                                              const double weight_values[]) {
  size_t proposal = 0;

  switch (variable.domain_type) {
    case DTYPE_BOOLEAN: {
      double potential_pos;
      double potential_neg;
      potential_pos = fg.potential(variable, 1, assignments, weight_values);
      potential_neg = fg.potential(variable, 0, assignments, weight_values);

      double r = erand48(p_rand_seed);
      // sample the variable
      // flip a coin with probability
      // (exp(potential_pos) + exp(potential_neg)) / exp(potential_neg)
      // = exp(potential_pos - potential_neg) + 1
      if (r * (1.0 + exp(potential_neg - potential_pos)) < 1.0) {
        proposal = 1;
      } else {
        proposal = 0;
      }
      break;
    }

    case DTYPE_CATEGORICAL: {
      varlen_potential_buffer_.reserve(variable.cardinality);
      double sum = -100000.0;
      proposal = Variable::INVALID_VALUE;
// calculate potential for each proposal given a way to iterate the domain
#define COMPUTE_PROPOSAL(EACH_DOMAIN_VALUE, DOMAIN_VALUE, DOMAIN_INDEX)       \
  do {                                                                        \
          for                                                                 \
      EACH_DOMAIN_VALUE {                                                     \
        varlen_potential_buffer_[DOMAIN_INDEX] =                              \
            fg.potential(variable, DOMAIN_VALUE, assignments, weight_values); \
        sum = logadd(sum, varlen_potential_buffer_[DOMAIN_INDEX]);            \
      }                                                                       \
    double r = erand48(p_rand_seed);                                          \
        for                                                                   \
      EACH_DOMAIN_VALUE {                                                     \
        r -= exp(varlen_potential_buffer_[DOMAIN_INDEX] - sum);               \
        if (r <= 0) {                                                         \
          proposal = DOMAIN_VALUE;                                            \
          break;                                                              \
        }                                                                     \
      }                                                                       \
  } while (0)
      // All sparse values have been converted into dense values in
      // FactorGraph.load_domains
      COMPUTE_PROPOSAL((size_t i = 0; i < variable.cardinality; ++i), i, i);

      assert(proposal != Variable::INVALID_VALUE);
      break;
    }

    default:
      // unsupported variable types
      std::abort();
  }

  return proposal;
}
```

```c++
void FactorGraph::sgd_on_variable(const Variable &variable,
                                  InferenceResult &infrs, double stepsize,
                                  bool is_noise_aware) {
  if (variable.is_boolean()) {
    // boolean: for each factor {learn}
    // NOTE: boolean vars do not support truthiness / noise-aware learning
    const VariableToFactor &vv = values[variable.var_val_base];
    for (size_t j = 0; j < vv.factor_index_length; ++j) {
      size_t factor_id = factor_index[vv.factor_index_base + j];
      sgd_on_factor(factor_id, stepsize, variable.id, variable.assignment_dense,
                    infrs);
    }
  } else {
    // categorical: for each evidence value { for each factor {learn} }
    size_t proposal = infrs.assignments_free[variable.id];
    for (size_t val = 0; val < variable.internal_cardinality(); ++val) {
      // skip non-evidence values
      if (!is_noise_aware && val != variable.assignment_dense) continue;

      const VariableToFactor &ev = values[variable.var_val_base + val];
      if (is_noise_aware && is_linear_zero(ev.truthiness)) continue;

      double truthiness = is_noise_aware ? ev.truthiness : 1;

      // run SGD on all factors "activated" by this evidence value
      for (size_t j = 0; j < ev.factor_index_length; ++j) {
        size_t factor_id = factor_index[ev.factor_index_base + j];
        sgd_on_factor(factor_id, stepsize * truthiness, variable.id, val,
                      infrs);
      }

      // run SGD on all factors "activated" by proposal value
      // NOTE: Current ddlog inference rule syntax implies that this list
      //       of factors would overlap the above list only if the factor
      //       connects tuple [var=val] and tuple [var=proposal], which sensible
      //       ddlog inference rules would never generate.
      //       Hence we assume that there is no overlap.
      //       This may change in the future as we introduce fancier factor
      //       types.

      // skip if we have just processed the same list of factors
      // NOTE: not skipping before the first loop because ... assignments_evid!
      if (val == proposal) continue;

      const VariableToFactor &pv = values[variable.var_val_base + proposal];
      for (size_t j = 0; j < pv.factor_index_length; ++j) {
        size_t factor_id = factor_index[pv.factor_index_base + j];
        sgd_on_factor(factor_id, stepsize * truthiness, variable.id, val,
                      infrs);
      }
    }  // end for
  }
}
```

```c++
// Inline by defined here; accessible only from current file.
inline void FactorGraph::sgd_on_factor(size_t factor_id, double stepsize,
                                       size_t vid, size_t evidence_value,
                                       InferenceResult &infrs) {
  const Factor &factor = factors[factor_id];
  if (infrs.weights_isfixed[factor.weight_id]) {
    return;
  }
  // stochastic gradient ascent
  // decrement weight with stepsize * gradient of weight
  // gradient of weight = E[f] - E[f|D], where D is evidence variables,
  // f is the factor function, E[] is expectation. Expectation is
  // calculated using a sample of the variable.
  double pot_evid = factor.potential(vifs.get(), infrs.assignments_evid.get(),
                                     vid, evidence_value);
  double pot_free = factor.potential(vifs.get(), infrs.assignments_free.get());
  double gradient = pot_free - pot_evid;
  infrs.update_weight(factor.weight_id, stepsize, gradient);
}
```


#### 2.3.3 

#### 2.3.4

