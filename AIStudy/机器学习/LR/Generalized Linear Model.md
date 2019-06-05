[TOC]

# Generalized Liear Model (广义线性模型)

## 1. 参考资料

1. [机器学习之回归（二）：广义线性模型](https://cloud.tencent.com/developer/article/1005793)
2. [GLM(广义线性模型) 与 LR(逻辑回归) 详解](https://blog.csdn.net/Cdd2xd/article/details/75635688)
3. [广义线性模型（Generalized Linear Model）](https://zhuanlan.zhihu.com/p/22876460)

## 2. 广义线性模型基础

不论是线性回归模型还是logistic回归，它们都是广义线性模型的特例。

线性回归中，我们假设：
$$y|x,\theta = N(\mu,\sigma^2)$$

logistic回归，我们假设：
$$y|x,\theta = Bernoulli(\phi)$$

分布的假设和回归模型有什么关系呢？

### 2.1 指数分布族

有如下形式的分布：
$$p(y;\eta) = b(y)exp(\eta^TT(y) - a(\eta))$$

其中：
$\eta$是自然参数
$T(y)$是充分统计量，一般$T(y) = y$
$a(\eta)$是log partition function。($e^{-a(\eta)}$充当规范化的作用，用于保证$\sum{p(y;\eta)} = 1$)

这里的T，a，b确定了一种分布，$\eta$是分布的参数。选择合适的T，a，b就能得到高斯分布和Bernoulli分布。

#### 2.1.1 伯努利分布转换为指数分布形式

$p(y=1;\phi) = \phi$；$p(y=0;\phi) = 1 - \phi$

$p(y;\phi) = \phi^y{(1-\phi)}^{1-y}$
$= exp(yln(\phi) + (1-y)ln(1-\phi))$
$= exp(yln{\frac{\phi}{1-\phi}} + ln(1-\phi))$

对照指数分布族公式：
$\eta = ln\frac{\phi}{1-\phi}$
$b(y) = 1$
$a(\eta) = -ln(1-\phi)$

#### 2.1.2 高斯分布$N(\mu, \sigma^2)$对一个的指数分布形式

$N(\mu,\sigma^2)$
$= \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{{(y-\mu)}^2}{2\sigma^2}}$
$= \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{{y^2 -2uy + \mu^2}}{2\sigma^2}}$
$= \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{y^2}{2\sigma^2}} e^{\frac{\mu y}{\sigma^2}-\frac{\mu^2}{2\sigma^2}}$

对照指数分布族公式可以得到：
$b(y) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{y^2}{2\sigma^2}}$
$a(\eta) = \frac{\mu^2}{2\sigma^2}$
$\eta = \frac{\mu}{\sigma^2}$

### 2.2 广义线性模型的假设

如果要通过广义线性模型解决问题，那么问题要满足如下的假设：

1. $y|x,\theta = ExponentialFamily(\eta)$，也就是说y的条件概率符合指数分布族。
2. 给定x的广义线性模型的目标是求解$T(y)|x$，不过很多情况是$T(y) = y$，所以问题就变成了$y|x$，也就是**希望拟合函数为$h(x)=E(y|x)$**
3. 自然参数$\eta$与$x$是**线性关系：$\eta=\theta^Tx$**。（$\eta$是向量时，$\eta_i=\theta^T_ix$）

## 3. 关于广义线性函数的基本问题

### 3.1 为什么要引入广义线性模型？

“回归”方法用于预测连续的值，如果直接用于解决离散的分类问题，效果就不是很好，或者说不能简单地直接使用回归模型。这个时候需要对回归方法的连续输出再做一层加工。这个多出来的过程就是GLM要解决的问题，这个处理过程的函数就叫做“连接函数”。

广义线性模型的处理流程图如下：
![glm](./images/GLM.png)

经过连接函数处理的广义线性模型既可以处理连续的回归问题，又可以处理离散的分类问题。

问题通过广义线性模型可以转换为获取合适的连接函数，以及有了连接函数，怎样获取预测函数$h_\theta(x)$。

### 3.2 连接函数如何求解？

连接函数满足一定特性时，才能称作广义线性模型。广义线性模型限定了X和Y必须满足指数分布族。

对任意 exponential family distribution，都存在 link function g(μ)=η。
