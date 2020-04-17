[TOC]

# Precision & Accuracy & Recall

| 真实值\\预测值 | P | N |
| - | - | - |
| T | True Positives | False Negatives |
| F | False Positives | True Negatives |

True Positives -> TP
False Negatives -> FN
False Positives -> FP
True Negatives -> TN

这三个指标都是围绕这四个量来计算的。

## 1. Precision

预测为正的样本中有多少是正确的。

$Precision = \frac{TP}{FP + TP}$

## 2. Accuracy

预测对的样本的比例。

$Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$

## 3. Recall

所有实际正样本中有多少被预测正确了，被预测出来了。

$Recall = \frac{TP}{TP + FN}$

## 4. 简单分析总结

一般情况下，召回率和精确率是针对某一个类别说的，比如正类别的Recall，负类别的Recall等。如果你是10分类，那么可以有1这个类别的Precision，2这个类别的Precision，3这个类别的Recall等。而没有类似全部数据集的Recall或Precision这种说法。 通常对于二分类，我们说正类的recall和precision。

## 5. F1-Score

为了平衡Recall和Precision，引入了二者的调和平均值。

$F1 = \frac{2 * Recall * Precision}{Recall + Precision}$