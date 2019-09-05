[TOC]

# Learning to rank

排序学习是将机器学习算法应用于信息检索的排序问题上。推荐排序的应用包括：搜索排序、广告排序、推荐排序。

## L2R训练算法

排序问题的解决办法总共有三大类：point wise、pair wise、list wise。

下面举例介绍三种划分对应的含义。假设我们要通过关键词来搜索文章，排序算法的目标就是对搜索到的文章进行排序。每个文档，我们都有一定的特征，目标值这三种类型却是不一样的。

### point wise

我们告诉排序算法的目标值是每个文档的得分，point wise算法是在这种前提下解决问题。

如果学习目标是给出预测文档一个实数值，那么就是回归问题。如果目标是一个概率预测，那么就是一个分类问题，比如CTR预估。

最直观的方案是Pointwise算法，例如对于广告CTR预估，在训练阶段需要标注某个文档的点击概率，这相对来说容易。

### pair wise

提供给排序算法的是任意两个文档的先后顺序。pair wise算法的目标是减少排序中逆序的数量，所以是一个二分类问题。

Pairwise算法一个重要分支是Lambda系列，包括LambdaRank、LambdaMart等，它的核心思想是：很多时候我们很难直接计算损失函数的值，但却很容易计算损失函数梯度（Gradient）。这意味着我们很难计算整个列表的nDCG和ERR等指标，但却很容易知道某个文档应该排的更靠前还是靠后。

### list wise

告诉排序算法文档的整体排名。Listwise算法的目标往往是直接优化nDCG、ERR等评价指标。

Listwise算法往往效果最好，但是如何为每个请求对所有文档进行标注是一个巨大的挑战。

## 排序算法的评价指标

### 1. P-R值

Precision和Recall，准确率与召回率。

### 2. DCG与nDCG

Discounted Cumulative Gain。

准确率和召回率有两个缺点：

- 对文档只区分相关与不相关，粒度太粗；
- 没有考虑文档排序的位置；

DCG可以解决这两个问题：

- 对文档的相关性划分多个相关性级别，rel1，rel2，rel3，...。
- 排序越靠后，评价指标越低。

$$DCG_p = \sum_{i=1}^p{\frac{2^{rel_i}-1}{log_2(i+1)}}$$

DCG没有进行normalization，不同的请求返回的列表长度不同，不同的搜索结果可比性不强。所以同常的会使用normalized DCG，即nDCG，它是DCG值再除以一个ideal DCG得到的。
$$nDCG = \frac{DCG_p}{IDCG_p}$$
其中，IDCG为：
$$IDCG_p = \sum_{i=1}^{|REL|}{\frac{2^{rel_i}-1}{log_2(i+1)}}$$
其中：REL表示相关性排序前p个结果。

### 3. ERR

Expected Reciprocal Rank。

ERR除了考虑当前排序文档的位置，还会考虑前面文档的相似性。
$$ERR = \sum_{r=1}^n\frac{1}{r}\prod_{i=1}^{r-1}(1-R_i)R_r$$

公式简单分析：$(1-R_i)$表示不相似性，$\prod$运算的作用就是考虑了排序，排序越靠后，那么对应乘积就会越小。

## 参考资源

1. [Learning to rank简介](https://www.cnblogs.com/kemaswill/archive/2013/06/01/3109497.html)
2. [ranking SVM](https://www.cnblogs.com/kemaswill/p/3241963.html)
3. [深入浅出排序学习：写给程序员的算法系统开发实践](https://tech.meituan.com/2018/12/20/head-in-l2r.html)
