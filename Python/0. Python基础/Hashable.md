[TOC]

# Python对象的Hashable

## Hashable官方文档定义

如果一个对象在其生命周期内，有一个固定的哈希值（这里需要__hash__()方法），并且可以与其他对象进行比较操作（这里需要__eq__()方法），那么就称这个对象是hashable。

所有Python内置的不可变对象都是hashable；可变容器，比如list、dict都是不可hash的。用户自定义的类的实例默认都是hashable；它们的hash值来自id()方法。

## Python对象的的可变性

当我们改变一个对象的值时，如果它的id值不发生变话，那么就称这个对象是可变的，否则就是不可变的。
