[TOC]

# 激活函数

## 1. 问题列表

1. 常用的激活函数有哪些？
2. 对比不同的激活函数，说明各自的利弊？
3. 为什么需要激活函数？
4. 如何选择激活函数？

## 2. 引用

[1. 常用激活函数总结](https://blog.csdn.net/tyhj_sf/article/details/79932893)

## 3. 激活函数基础知识

下面逐个介绍激活函数，介绍其公式、图像，及其优点和缺点。

### 3.1 Sigmoid函数

数学公式为：
$$f(z) = \frac{1}{1+e^{(-z)}}$$

Sigmoid曲线如下：
![sigmoid](./images/activation/sigmoid.png)

特点：
输出在(0,1)区间，很大的负数时，输出接近0；很大的正数时，输出接近1。远离0的值对应的导数接近0。

缺点：
sigmoid函数曾经被大量使用，但是现在使用它的人越来越少了。主要是因为它自身的一些缺点。

1. 容易导致梯度消失。

我们先来看看sigmoid的导数曲线，然后再介绍为什么会出现梯度消失的问题。
![sigmoid-derivative](./images/activation/sigmoid-derivative.png)

从图中我们可以看出，sigmoid的导数取值在$(0,0.25]$之间。

然后我们在以一个简单的网络来说明反向传播过程，以此来说明为什么梯度会消失。

下面是一个有三个隐藏层，每一层只有一个神经元。
![simple-network](./images/activation/simple-network.png)

$w_1,w_2,...$是权重，$b_1,b_2,...$是偏差。$C$是损失函数。输出$a_j$是第j层的神经元的输出。
公式为：$\sigma(z_j)$，其中$z_j = w_ja_{j-1} + b_j$

$C = loss(a_4)$
$= \sigma(w_4a_3+b_4)$
$= \sigma(w_3\sigma(w_4a_3+b_4) + b_3)$
$= ...$

我们从上面的式子可以看出，最外层的损失函数是激活函数的多层复合函数，意味着如果我们要对最开始的参数比如$b_1,w_1$求偏导，那么，根据复合函数求导的原则，这个式子中会有很多的$\sigma(z_j)$相乘。
![sigmoid-vanishing](./images/activation/sigmoid-vanishing.png)

从上面可以看出，由于sigmoid的导数的取值范围是$(0,0.25]$，特别是当变量取值稍微远离0一些，那么导数就是接近于0。如果网络层数深一些，那么同样也会导致梯度在反向传播时逐渐为0。这其实意味着损失函数的变化是不能传递给最开始网络层的参数的。

2. Sigmoid的输出不是0均值(zero-centered)。

sigmoid的输出都是大于0，当上一层的sigmoid输出传递给下一层时，会经过一个线性变换：$f = w^Tx+b$。如果我们对$w$求导，我们发现导数x都是大于0，具有一致的符号，那么$w$的更新也会沿着一个方向更新。这样不利于训练结果的收敛。

3. 解析式中包含幂运算，对于计算机而言是比较耗时的。

### 3.2 tanh函数

tanh的解析式如下：
$$tanh(x) = \frac{e^x - e^{-x}}{e^x+e^{-x}}$$

对应的曲线和导数的曲线如下图：
![tanh](./images/activation/tanh.png)

它解决了sigmoid的zero-centered的问题，但是梯度消失的问题并没有解决，同样也是需要幂运算。

### 3.3 Relu函数

Relu函数的解析式如下：
$$Relu = max(0,x)$$

Relu函数的曲线和导数的曲线如下：
![relu](./images/activation/relu.png)

注意：
Relu函数不是全区间可导，但是在实际问题的有意义区间内是可导的。

Relu函数虽然简单，却有如下优点：

1. 解决了gradient vanishing的问题。
2. 计算简单，速度快。
3. 收敛速度远快于sigmoid和tanh。

但同时也存在如下问题：

1. 不是zero-centered。
2. Dead Relu Problem，也就是有些神经元永远不会被激活，导致相应的参数无法得到更新。导致这种情况的原因有：
(1). 非常不幸的参数初始化，这种情况比较少，可以使用Xavier初始化方法。
(2). learning rate太大，导致训练过程参数更新太大，进入这种状态。避免方法就是不要使用太大的learning_rate，或者使用adagrad等自动调节learning_rate的方法。

尽管存在这些问题，Relu仍旧是常用的激活函数，搭建nn时也应该优先尝试。

### 3.4 Leaky Relu函数

函数表达式：
$$f(x) = max(\alpha x,x)$$

函数曲线和导数曲线如下：
![leaky-relu](./images/activation/leaky-relu.png)

为了解决Relu的dead relu problem而提出的将Relu前半部分设置为$\alpha x$，而不是0，同常$\alpha = 0.01$。还有一种做法就是让$\alpha$参数也通过反向传播学习。

虽然理论上Leaky Relu克服了Relu的缺陷，但是实际使用中并没有完全证明Leaky Relu总是好于Relu。

### 3.5 ELU(Exponential Linear Units)函数

函数表达式：
$$f(x) = \begin{cases}
x& \text{x>0} \\
\alpha(e^x - 1)& \text{otherwise}
\end{cases} $$

函数曲线和导数曲线如下图：
![elu](./images/activation/elu.png)

ELU的优点就是：

1. 不会出现Dead Relu问题；
2. 输出接近于zero-centered。

缺点就是计算量稍大。

### 3.6 Maxout函数

可以参考论文：《maxout networks》

Maxout是深度学习中的一层网络，类似于池化层、卷积层一样。我们可以把maxout看做是网络的激活函数层。

关于maxout有专门的一节来介绍，这里不再详细说明。

## 4. 激活函数相关问题

### 4.1 为什么引入激活函数？

如果没有引入激活函数，那么神经网络的层与层之间只有线性变换，不论多少层的线性变化，都等价于一层的线性变化。那么，模型的表达能力或者说拟合能力就很有限，相当于一个感知机模型。

通过引入非线性激活函数，可以增加网络的表达能力，可以几乎逼近任意函数。这样，可以用神经网络模型解决更为复杂的问题。

### 4.2 有哪些激活函数？

常用的激活函数如前面介绍的内容。

### 4.3 如何选择激活函数？

1. 深度学习往往需要大量的处理时间，所以模型的收敛速度就尤为重要。总体上来讲，训练深度模型，尽量使用zero-centered的数据和zero-centered的输出。这样可以加快模型的收敛。
2. 如果使用Relu，那么就需要小心设置learning_rate，避免出现dead神经元。如果问题不好解决，可以考虑使用leaky relu、ELU或者maxout。
3. 最好不要使用sigmoid，可以试试tanh。
