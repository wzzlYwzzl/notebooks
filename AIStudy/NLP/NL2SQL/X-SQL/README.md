[TOC]

# X-SQL

X-SQL是微软的Dynamic 365提出的一种方案，同样是将预测SQL分解为6个子任务。

另外，包括以下几点的改进：

1. 使用MT-DNN作为编码层，取代了SQLova的BERT。
2. 将SQLova中的两个Segmentation:Question Seg和Column Seg扩展成了四个：Question、Categorical Column、Numerical Column、Empty Column这四种Segmentation Embedding，分别用来对自然语句问句、文本类型的列、数字类型的列以及空列的相应输入。
