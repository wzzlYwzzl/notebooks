[TOC]

# JPype

JPype是一个Python模块，它允许在Python中完全访问Java。它允许Python使用纯Java的库，探索和可视化Java结构，开发和测试Java库，科学计算，等等。它可以很好的平衡：Python的快速原型开发和Java的强类型、高性能的产品级代码。

这不是通过像Jython那样重新实现Python来实现的，而是通过两个虚拟机中本机级的接口实现的。 这种基于共享内存的方法可实现不错的计算性能，同时提供对整个CPython和Java库的访问。