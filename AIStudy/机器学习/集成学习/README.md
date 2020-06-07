[TOC]

# 集成学习

集成学习的核心思想就是将多个**弱学习器**经过**一定方式组合**在一起构成一个**强学习器**。通俗表达就是“三个臭皮匠，顶一个诸葛亮”。

集成学习最早来源于Valiant提出的PAC(Probably Approximately Correct)学习模型，该模型中首次定义了弱学习器和强学习器的概念。**弱学习器**：准确率比随机猜测高一些的学习算法；**强学习器**：准确率很高且能在多项式时间内完成的学习算法。该模型提出了给定任意的弱学习算法，能否将其提升为强学习算法的问题。1990年，Schapire对其进行了肯定的证明。

目前集成学习中的“一定组合方式”包括：Voting、Averaging、Bagging、Boosting、Stacking和Blending。

![1](./images/1.png)

## 1. Voting

一种很简单的集成思路，主要用于离散的分类问题。

包括：

1. 绝对多数投票法
投票超过半数的标记才会采用，否则拒绝。

2. 相对多数投票法
采用投票数量最多的标签，若同时有多个标签投票一致，则随机选取一个。

3. 加权投票法
为标记赋以不同的权重，可以理解为这是一种先验知识，然后再利用相对多数投票法。

Voting做法应该算是一种很泛的思想，它没有说明具体每个投票学习器的具体应该如何获取，也没有对具体学习器获取做任何限制。

## 2. Averaging

取平均，通常用于回归问题。

常见的Averaging方法：

1. 简单平均
2. 加权平均

这是应对回归问题的最简单直接的集成思想。

## 3. Bagging

Bootstrap Aggregation的简称。

**基本思路**：

对数据集进行有放回采样，得到多个数据集的随机采样子集，用这些随机子集分别对多个学习器进行训练，最终得到多个学习器。对于分类问题，多个学习器通过Voting的做法得到最终结果，对于回归问题，可以采用Averaging的做法。

Bagging一般使用强学习器，学习器之间不存在依赖关系，可以实现并行。这一点和Boosting算法是有不同的，Boosting倾向于用弱学习器来达到强学习器的效果。

Bagging的代表方法就是Random Forest。

## 4. Boosting

Boosting的思想核心：新的弱学习器基于前一个学习器的效果来进行调整，学习得到新的模型，最后将得到的多个学习器组合成一个学习器。

Boosting算法是一个串行优化的过程。

1995年，Freund等人提出了**AdaBoost算法**。1999年，Friedman提出了**Gradient Boosting算法**。这两种是Boosting思想的两大经典算法。

## 5. Stacking

stacking模型的结构：

整个stacking模型

单个模型的单层处理过程：
![2](./images/2.png)

stacking多个模型的单层处理过程：
![3](./images/3.jpg)

## 6. Blending

## 参考

1. [集成学习之Blending(模型混合)](https://www.jianshu.com/p/b95f9e36dfef?utm_source=oschina-app)
2. [Ensemble Learning常见方法总结（Bagging、Boosting、Stacking、Blending）](https://blog.csdn.net/FrankieHello/article/details/81664135)
3. [集成学习之Boosting —— AdaBoost原理](https://www.cnblogs.com/massquantity/p/9063033.html)
4. [集成学习总结 & Stacking方法详解](https://blog.csdn.net/willduan1/article/details/73618677)
5. [模型融合：stacking&blending](https://blog.csdn.net/choven_meng/article/details/82913757)
