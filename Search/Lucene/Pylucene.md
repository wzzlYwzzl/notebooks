[TOC]

# Pylucene

## Pylucene工作原理

PyLucene 是在 Python 程序中嵌入了一个 JVM 来使用 Lucene，这个工作主要通过 JCC 来完成，JCC 编译 Lucene 源码为 C++，然后在 Python 中通过 JNI 进行调用。

PS. 要了解JNI，请到(../Java/JNI)目录了解。

## Pylucene自定义Analyzer

[参考链接](https://blog.csdn.net/thuyx/article/details/70596428)
