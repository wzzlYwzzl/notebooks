[TOC]

# Dropout

## 1. 参考资源

[1. Improving neural networks by preventing co-adaptation of feature detectors](https://arxiv.org/abs/1207.0580v1)
[2. Dropout:A Simple Way to Prevent Neural Networks from Overfitting](http://jmlr.org/papers/v15/srivastava14a.html)
[3. 深度学习中Dropout原理解析](https://blog.csdn.net/program_developer/article/details/80737724)

## 2. Dropout基本介绍

### 2.1 Dropout出现的原因

不论在机器学习还是深度学习中，当模型复杂，表达力强，但是用于训练模型的样本有不足时，就会很容易出现过拟合现象。

解决这种过拟合问题的一种做法就是采用“集成学习”模型，就是训练多个模型，然后组合得到最终的模型。

对于深度学习模型，Dropout就是一个用于缓和过拟合问题的一种解决方案。

### 2.2 什么Dropout？

在神经网络的训练过程中，每个batch的训练中，以一定的概率$1-p$对隐藏层的每一层神经元临时设置输出为0，也就是一定的概率让网络中的神经元在一个batch的训练中不起作用。以此，训练得到最终的网络。

直观描述如下图：
![droput1](./images/dropout/dropout1.png)

### 2.3 Dropout具体计算过程

1. 训练过程

没有使用Dropout和使用Dropout对比：
![dropout2](./images/dropout/dropout2.png)

没有使用Dropout时计算公式如下：
$$z_i^{l+1} = w_i^{l+1}y^l$$ $$y_i^{l+1} = f(z_i^{l+1})$$

使用Dropout时的计算公式如下：
$$r_j^{l} = Bernoulli(p)$$ $$
\widetilde{y}^{l+1} = r^{(l)} * y^{(l)}$$ $$
z_i^{(l+1)} = w_i^{(l+1)} + b_i^{(l+1)}
$$ $$
y_i^{(l+1)} = f(z_i^{(l+1)})
$$

2. 测试过程

由于在训练过程中，神经元是以p概率变为0，所以测试时，参数的权重也需要乘以p。
$$w_{test}^{(l)} = (1-p)W^{(l)}$$

**注意**：测试阶段是否乘以p，取决于在训练的时是否对$y_i$进行缩放，如果进行了，那么在测试阶段就没有必要**权重乘以p**。训练阶段对$y_1,...,y_n$进行缩放，是乘以$\frac{1}{1-p}$，以保证输出的期望值保持不变。

### 2.4 关于Dropout的简单总结

Dropout被大量应用于全连接网络，在卷积网络隐藏层中，由于卷积自身稀疏以及稀疏化的ReLu函数的大量使用的原因，Dropout策略在卷积网络隐藏层中使用较少。Dropout作为一个超参，需要根据具体的网络和具体的应用场景进行尝试。

## 3. Dropout相关的问题

### 3.1 为什么说Dropout可以解决过拟合问题？

1. 相当于训练多个模型，取平均的作用。
dropout掉不同的隐藏神经元就类似在训练不同的网络，随机删掉一定比例的隐藏神经元导致网络结构已经不同，整个dropout过程就相当于对很多个不同的神经网络取平均。而不同的网络产生不同的过拟合，一些互为“反向”的拟合相互抵消就可以达到整体上减少过拟合。

另一种解释是通过dropout，隐藏层的神经元被随机丢失，那么输出层无法过度、一直依赖某个固定的隐藏层单元，那么就会比较均衡地修改不同的神经元参数，从而起到正则化的作用。

2. 减少神经元之间复杂的共适应关系。
因为dropout程序导致两个神经元不一定每次都在一个dropout网络中出现。这样权值的更新不再依赖于有固定关系的隐含节点的共同作用，阻止了某些特征仅仅在其它特定特征下才有效果的情况。迫使网络去学习更加鲁棒的特征，这些特征在其它的神经元的随机子集中也存在。换句话说假如我们的神经网络是在做出某种预测，它不应该对一些特定的线索片段太过敏感，即使丢失特定的线索，它也应该可以从众多其它线索中学习一些共同的特征。从这个角度看dropout就有点像L1，L2正则，减少权重使得网络对丢失特定神经元连接的鲁棒性提高。

### 3.2 Dropout存在的问题？

减慢收敛速度，因为每次只会更新一部分参数，下次可能更新的参数和上次不一样，意味着同一个参数要想被更新两次，可能需要多个batch的训练。

### 3.3 为什么进行Dropout时，要对神经元的权重进行缩放？

训练的时候我们时丢弃了一些神经元，但是在测试时时无法丢弃神经元的，因为丢弃神经元会带来不稳定。

但是，如果我们直接使用训练好的网络，那么训练模型和测试模型就会出现不对等，那么得到的结果肯定是有问题的。就好比训练时的网络结构和测试时的网络结构不一致一样。

为了模拟训练的做法，就以一定概率对权重进行缩放，以使最后每一层**网络的权重的期望和训练时**时一样的，更本质的原因是让每一层网络的输出的期望值一样。

## 4. Dropout Pytorch实现

```python
import torch
import torch.nn as nn
import numpy as np

def dropout(X, drop_prob):
    X = X.float()
    keep_prob = 1 - drop_prob

    if keep_prob == 0:
        return torch.zeros_like(X)
    mask = (torch.rand(X.shape) < keep_prob).float()
    return mask * X / keep_prob
```
