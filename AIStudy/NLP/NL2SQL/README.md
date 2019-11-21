[TOC]

# NL2SQL

NL2SQL的任务就是将自然语言转换为有严格语法格式的SQL语句。

下面以在WikiSQL数据集上的模型算法来梳理NL2SQL问题有哪些解决方案。最新解决方案可以参考[WikiSQL~github](https://github.com/salesforce/WikiSQL)

## 1. 弱监督学习解决方案

由于标注数据同常是一件高成本且困难，所以如果解决问题时，如果能够采用弱监督，甚至无监督，若能够取得还可以的效果，都是值得去分析、研究的。但是，和有监督的模型相比，无监督的效果目前来说都是弱于有监督算法的。

目前榜单上只有三个：Rule-SQL、MAPO、MeRL。

## 2. 有监督学习解决方案

目前(2019-10-16)表现最好的监督模型是SQLova、X-SQL。

## 数据集

1. [WikiSQL](https://github.com/salesforce/WikiSQL)
2. 追一科技在天池NL2SQL精彩中提供的数据。(暂时没链接)
3. Spider
