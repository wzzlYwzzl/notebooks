[TOC]

# Python2与Python3的区别

[Python2和Python3的差异](https://www.cnblogs.com/feifeifeisir/p/9599218.html)

## 1. 核心类差异

### 编码与字符串

### import

### 新式类与老式类

### 缩进

## 2. 废弃类差异

### print函数

python2中的print语句被废弃，统一使用print函数。

### exec语句

python2中的exec语句被python3废弃，统一使用exec函数。

### execfile

execfile被python3废弃，推荐使用exec(open("./filename").read())

### 不相等操作符<>

<>不相等符号被废弃，统一使用"!="。

### long整数类型

long类型被python3废弃，统一使用int。

### xrange函数

xrange被python3废弃，统一使用range

### 不再返回list对象

dictionary关联的keys()、values()、items()、zip()、map()、fiter()，这些方法返回的对象不再是list，但是可以通过list()将其转换为list。

### 迭代器的next函数


