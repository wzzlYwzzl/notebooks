[TOC]

# TLAB

TLAB，Thread Local Allocation Buffer。TLAB是线程专用的内存分配区域，每个线程会核心维护相关的三个参数：start、top、end，用于标识TLAB区域的的三个位置，类似于栈的指针一样。TLAB维护的区域还是在堆上，具体而言就是在Eden区中。

## 1. 为什么需要TLAB

这是为了**加速对象的分配**。由于对象一般分配在堆上，而堆是线程共用的，因此可能会有多个线程在堆上申请空间，而每一次的对象分配都必须线程同步(虚拟机采用CAS配上失败重试的方式保证更新操作的原子性)，会使分配的效率下降。考虑到对象分配几乎是Java中最常用的操作，因此JVM使用了TLAB这样的线程专有区域来**避免多线程冲突**，提高对象分配的效率。

## 2. TLAB分配策略

　一个100KB的TLAB区域，如果已经使用了80KB，当需要分配一个30KB的对象时，TLAB是如何分配的呢？

此时，虚拟机有两种选择：

- 第一，废弃当前的TLAB（会浪费20KB的空3.4 间）；
- 第二，将这个30KB的对象直接分配到堆上，保留当前TLAB（当有小于20KB的对象请求TLAB分配时可以直接使用该TLAB区域）。

JVM选择的策略是：在虚拟机内部维护一个叫refill_waste的值，当请求对象大于refill_waste时，会选择在堆中分配，反之，则会废弃当前TLAB，新建TLAB来分配新对象。

默认情况下，TLAB和refill_waste都是会在运行时不断调整的，使系统的运行状态达到最优。

## 3. TLAB的优缺点

优点在`为什么需要TLAB`中有说明了，这里主要给出TLAB的局限性：

- TLAB空间一般不会太大，所以大对象无法进行TLAB分配，只能分配到堆上。

- TLAB的大小是固定的，TLAB允许浪费空间，对应于`最大浪费空间`参数可以设置；这就会倒置Eden区的空间不连续。

## 4. TLAB相关的JVM参数

- -XX:+UseTLAB 使用TLAB

- -XX:+TLABSize 设置TLAB大小

- -XX:TLABRefillWasteFraction设置维护进入TLAB空间的单个对象大小，他是一个比例值，默认为64，即如果对象大于整个空间的1/64，

- -XX:TLABWasteTargetPercent设置TLAB空间所占用Eden空间的百分比大小 默认是1%

- -XX:+PrintTLAB 查看TLAB信息

- -XX:ResizeTLAB 自调整TLABRefillWasteFraction阈值。

## 5. TLAB扩展，栈上分配

下面给出一个JVM为对象分配内存的流程图：

![1](./images/TLAB/1.png)

为了优化JVM的内存管理效率，除了使用TLAB外，还有一种策略：**栈上分配**。

顾名思义，就是将对象直接分配到栈上。

**优点**：

- 可以在函数调用结束后自行销毁对象，不需要垃圾回收器的介入，有效避免垃圾回收带来的负面影响；
- 栈上分配速度快，提高系统性能

**局限性**：

栈空间小，对于大对象无法实现栈上分配。

**技术基础**：

逃逸分析：判断对象的作用域是否超出函数体[即:判断是否逃逸出函数体]。

### 5.1 一个测试例子

```java
package com.blueStarWei.templet;

public class AllotOnStack {

    public static void main(String[] args) {
        long start = System.currentTimeMillis();
        for (int i = 0; i < 100000000; i++) {
            alloc();
        }
        long end = System.currentTimeMillis();
        System.out.println(end - start);
    }

    private static void alloc() {
        User user = new User();
        user.setId(1);
        user.setName("blueStarWei");
    }
}
```

使用如下参数运行，发现不会触发GC：

```txt
-server -Xmx15m -Xms15m -XX:+DoEscapeAnalysis -XX:+PrintGC -XX:-UseTLAB -XX:+EliminateAllocations
```

使用如下参数（任意一行）运行，会发现触大量GC：

```txt
//不使用逃逸分析
-server -Xmx15m -Xms15m -XX:－DoEscapeAnalysis -XX:+PrintGC -XX:-UseTLAB -XX:+EliminateAllocations

//不使用标量替换
-server -Xmx15m -Xms15m -XX:＋DoEscapeAnalysis -XX:+PrintGC -XX:-UseTLAB -XX:－EliminateAllocations
```

可以发现：栈上分配依赖于逃逸分析和标量替换。
