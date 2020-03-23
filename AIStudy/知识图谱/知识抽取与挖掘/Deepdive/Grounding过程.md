[TOC]

# Deepdive Factor Graph Grounding

Grounding是构建因子图，并持久化到文件中的一个过程，得到的这个因子图描述文件供后面的sampler使用。

Grounding过程会生成四种类型的文件：

- variables文件，定义因子图的变量；
- factors文件，定义不同的因子；
- weights文件，定义因子的权重；
- metadata文件，描述文件；

上面四种类型的文件，前三种都是二进制文件，最后一个是文本文件。

## Weights文件格式

```txt
weightId        long    8
isFixed         bool    1
initialValue    double  8
```

## Variables文件格式

```txt
variableId      long    8
isEvidence      bool    1
initialValue    double  8
dataType        short   2
edgeCount*      long    8
cardinality     long    8
```

## Factors文件格式

```txt
weightId        long    8
factorFunction  short   2
equalPredicate  long    8
edgeCount       long    8
variableId1     long    8
isPositive1     bool    1
variableId2     long    8
isPositive2     bool    1
...

# from version 0.03, the edgeCount field in Variables is always -1.
```

## metadata文件格式

```txt
Number of weights
Number of variables
Number of factors
Number of edges
Path to weights file
Path to variables file
Path to factors file
Path to edges file
```

## 增量Grounding，文件格式

对于增量的grounding，weights、variables、meta文件格式一样，还会有两个文件格式有区别：

### Factor文件格式

```txt
factorId        long    8
weightId        long    8
factorFunction  short   2
edgeCount       long    8
```

### Edges文件格式

```txt
variableId      long    8
factorId        long    8
position        long    8
isPositive      bool    1
equalPredicate  long    8
```

## 参考

1. [官方介绍](http://deepdive.stanford.edu/factor_graph_schema)
