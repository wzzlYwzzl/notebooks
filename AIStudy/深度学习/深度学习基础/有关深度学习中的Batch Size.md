[TOC]

# Batch Size

## 1. 引用

[1. 谈谈深度学习中的Batch Size](https://blog.csdn.net/haima1998/article/details/80026072)
[2. 关于深度学习中的Batch Size](https://www.cnblogs.com/gengyi/p/9853664.html)

## 2. Batch Size基础

Batch Size是在训练深度学习网络时一个很重要的超参。它直接影响着我们训练的模型是否能够快速收敛，得到满足需求的最优参数。

Batch Size的取值在两个极端范围之间：
一个就是batch_size = 1，也就是一次用一个训练样本进行参数更新，这个称为online learning；
另一个极端就是一次使用所有的样本训练，也就是full batch learning。

合理的Batch Size就是用于调和两个极端情形下的存在的不足。下面先分析这两个极端情况下进行训练的优缺点。

### 2.1 batch_size=1(online learning)

由于每次使用一个样本进行学习，对每一步的梯度方向的估计会不准确，每次修正梯度方向也不是最优的，导致训练结果不停地波动，难以达到收敛。

效果如下图：
![online-learning](./images/batchsize/online-learning.png)

### 2.2 Full-Batch Learning

先说优点吧，使用所有样本，会对整体样本有一个更为准确的估计，那么我们会得到更为准确的梯度更新方向。学习过程中的波动就会很小，更容易收敛。(优点：学习方向准确，波动小)

接下来就要谈谈这种做法带来的问题：

如果使用所有样本进行一个Batch的训练，一个最直接的影响就是会耗费更多的内存或者显存，因为同时涉及更多矩阵的运算，保存更多的变量。(1.耗费内存或显存)

由于我们在训练是会设定一个相对比较小的learning_rate，意味着每batch的训练，只能沿着正确的方向学习一小步，这就导致我们不得不训练多个epoches，才能得到最终的最优参数。问题在于，同常每个batch，我们不需要所有的训练样本就能够对梯度方向有一个正确的估计了，再大的batch_size只会带来负面的影响，比如训练时间会增长。(2.不必要，反而让训练时间更长)

比如，利用LeNet训练Mnist数据集，修改不同的Batch Size，对比结果如下：
![batch-size-compare](./images/batchsize/batch-size-compare.png)

从中我们可以发现，Batch Size不是越大越好的。

### 2.3 合理的Batch Size

先给出一个对比图，说明不同batch_size的训练波动情况：
![batch-compare](./images/batchsize/batch-compare.png)

其中：
红色：batch_size = 1
绿色：batch_size = 100;
蓝色：batch_size = 1100;（全部数据集）

Batch Size大的相对小的，更为稳妥，效果更好，大得多了，可能是不必要的，但是不会带来直接影响最终结果的负面影响，太大的负面影响不是关键的，除非是机器内存无法承受，否则增大Batch_size是可以的。

相反，如果Batch_size过小，反而会影响训练效果。所以，最合理的Batch Size是需要根据实际情况，做对比试验得到的。这样既能充分利用内存，有不会导致训练过程波动很大，又能加快训练过程。