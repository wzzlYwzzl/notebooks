[TOC]

# PageRank算法介绍

## 简单介绍

PageRank是Google创始人Larry Page创建的网页排序算法。

PageRank算法作用就是对网页的排序进行调整。Google搜索对搜索进行排序的大致过程如下：

> 1. 找到所有与搜索关键词匹配的网页
> 2. 根据网页的页面因素，比如标题、关键词密度等排列等级
> 3. 计算导入链接的锚文本中关键词
> 4. 通过pagerank得分调整网站的排名结果

上面的这个过程只是粗略的概括，实际过程要比这个复杂。

## 基本思想

> 1. 数量假设：一个网页被链接的数量越多，那么说明它越重要。
> 2. 质量假设：一个网页被越重要的网页链接，那么说明它越重要。但是，一个网站如果链接其他网站过多，那么它分配给其他网站的PR值就越低。

## 缺点

> 1. pagerank没有考虑搜索的主题特征；
> 2. 旧的网页相对新的网页有更高的PR值；

## 参考

1. [深入探讨pagerank(一)](https://blog.csdn.net/MONKEY_D_MENG/article/details/6554518)
2. [深入探讨pagerank(二)](https://blog.csdn.net/monkey_d_meng/article/details/6556295)
3. [pagerank快速入门](http://baijiahao.baidu.com/s?id=1601233403833910471&wfr=spider&for=pc)
4. [pagerank简介](https://www.cnblogs.com/smuxiaolei/p/7614287.html)
