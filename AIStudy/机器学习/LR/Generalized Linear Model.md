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


对照指数分布族公式可以得到：


### 2.2 广义线性模型的假设

如果要通过广义线性模型解决问题，那么问题要满足如下的假设：

1. $y|x,\theta = ExponentialFamily(\eta)$，也就是说y的条件概率符合指数分布族。
2. 给定x的广义线性模型的目标是求解$T(y)|x$，不过很多情况是$T(y) = y$，所以问题就变成了$y|x$，也就是希望拟合函数为$h(x) = E(y|x)$
3. 自然参数$\eta$与$x$是线性关系：$\eta = \theta^Tx$。（$\eta$是向量时，$\eta_i = \theta^T_ix$）