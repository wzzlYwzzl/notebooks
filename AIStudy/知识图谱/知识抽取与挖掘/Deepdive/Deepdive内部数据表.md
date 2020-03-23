[TOC]

# Deepdive内部使用的数据库表和视图

Deepdive不同过程之间的数据流是通过数据库表或者视图来完成的，有些输入数据的表是由用户自己指定创建的，有些则是内部流程创建的中间表，要保证自己创建的表不能和这些表和视图重名。

## Deepdive内部表和视图

 Schema | List of relations Name | Type
| - | - | - |
 public | dd_graph_variables_holdout                   | table
 public | dd_graph_variables_observation               | table
 public | dd_graph_weights                             | table
 public | dd_inference_result_variables                | table
 public | dd_inference_result_weights                  | table
 public | dd_inference_result_weights_mapping          | view
 public | dd_factors_[RULE_NAME]                       | table
 public | dd_weights_[RULE_NAME]                       | table
 public | [TABLE]_[VARIABLE]_inference                 | view
 public | [TABLE]_[VARIABLE]_calibration               | view
 public | dd_categories_[TABLE]                        | view

where [RULE_NAME] is the name of an inference rule, [TABLE] is the name of a table that contains variables, and [VARIABLE] is the name of a variable in the corresponding table.

## 内部表和视图说明

Description of each schema:

- **dd_graph_variables_holdout:** a table that contains all variable ids that are used for holdout. Can be used for custom holdout by a holdout query.

- **dd_graph_variables_observation:** a table that contains all variable ids that are evidence that will not be fitted during learning. An usage example of this table can be found here.

- **dd_graph_weights:** a table that contains all the materialized weights.

- **dd_inference_result_variables:** a table that contains the inference results (expectation) for all query variables.

- **dd_inference_result_weights:** a table that shows factor weight ids and learned weight values.

- **dd_inference_result_weights_mapping:** a view that maps all distinct factor weights to their description and their learned values. It is a commonly used view that shows the learned weight value of a factor as well as the number of occurences of a factor.

- **dd_factors_[RULE_NAME]:** a table that is defined by the input query of an inference rule. You can use it as a feature table in BrainDump.

- **dd_weight_[RULE_NAME]:** a table that stores initial weights for factors, used internally.

- **[TABLE]_[VARIABLE]_inference:** a view that maps variables with their inference results. It is commonly used for error analysis.

- **[TABLE]_[VARIABLE]_calibration:** a view that has calibration statistics of a variable. Used in generating calibration plots.

- **dd_categories_[TABLE]:** a view that records the cardinality series of given variable. For example if the domain of a variable is {1,2,3} the cardinality is 3.

## 参考

1. [官方说明文档](http://deepdive.stanford.edu/reserved_tables)
