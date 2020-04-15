[TOC]

# Spring定时任务

用Java语言实现定时任务有如下三种方式：

- Java自带的java.util.Timer类。这种方式允许让你的程序按照某个频度执行，但是不能指定执行时间。这种方式较少使用。
- Quartz。这是一个功能强大的调度器，允许程序按照某个频率执行，也允许指定某个时间执行。使用起来需要继承org.springframework.scheduling.quartz.QuartzJobBean，配置稍显复杂，所以，一般会使用spring集成quartz。
- Spring3.0之后的自带task，即Spring Schedule。可以把它看做一个轻量级的Quartz，使用方法也很简单。可以参考已经整理的[Spring boot定时任务](./Spring%20Boot/Spring%20Boot定时任务.md)。

下面主要介绍spring-quartz这种方式，spring schedule的方式已经整理过了。

## 1. Spring Quartz定时任务
