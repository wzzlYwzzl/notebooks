[TOC]

# whoosh的Analyzer

## 什么是Analyzer

在whoosh中，一个Analyzer就是一个function，或者是一个callable(也就是实现了__call__方法)的class，调用它能够将输入的unicode字符串加工成tokens。所谓的token，就是用于构建索引时使用的最小term。

Analyzer同常是封装了一个tokenizer和零个或者多个filter。Analyzer会把输入__call__的参数传给tokenizer，而tokenizer通常也会被filter所包裹。

## 什么是Tokenizer

是一个callable的对象，输入是unicode的string，输出是一系列的analysis.Token。

## 什么是Filter

一个callable的对象，输入是tokens，输出是tokens。

## Analyzer如何使用

在创建schema时，指定field使用哪个analyzer。

```python
schema = Schema(content=TEXT(analyzer=StemmingAnalyzer()))
```
