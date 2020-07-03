[TOC]

# mount命令性能优化

这里之所以创建一个文档，就是为了提醒自己，mount命令是有优化空间的，可以控制mount的一些行为，提高文件系统的性能。

比如：mount时，除了使用defaults参数外，添加noatime、nodiratime、nobarrier等，可以改善性能。

具体的优化使用时再仔细学习吧。

## 参考

1. [Linux 文件时间记录属性 调优](https://www.cnblogs.com/xiangsikai/p/9505842.html)
