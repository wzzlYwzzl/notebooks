[TOC]

# Python不定数量函数参数

同常我们定义函数，都是如下形式：

```python
def func(a,b,c):
    pass
```

但是，如果我们不确定，或者是不关心参数的数量时，我们就应该采用不定数量参数形式的函数定义了。

不定量参数有两种形式：一种是前面一个\*，比如“\*args”，这里args可以换成其他名字，args只是约定俗称的表示，核心是前面的\*；另一种是前面有两个\*号，比如\*\*kwargs。

## *和**号有什么用

其实*号和**号都有两个作用，一个是打包，另一个是拆包。下面分别距离介绍。

### *打包

```python
def fun(a,b,*args):
    pass

#调用fun函数：
fun(1,2,4,5,6)

#这个时候args=(4,5,6)，这里*体现的作用就叫做打包。
```

### *拆包

```python
def fun(a,b,c):
    pass

#调用前面的函数
fun(*[1,2,3])

#这里体现的作用就是将list拆包为三个参数。
```

### **打包

```python
def fun(**nums):
    print(nums)

fun(a=1,b=2,c=3)

#输出是{'a':1, 'b':2, 'c':3}
```

### **拆包

```python
def fun(a,b,c):
    pass

#调用函数，这里体现拆包
fun(**{'a':1, 'b':2, 'c':3})
```

## 这两种形式有何区别

*args是将参数作为tuple的形式供函数使用的。
**kwargs是将参数打包为dict供函数使用。

## args、*args、**kwargs的使用顺序

必须是func(args, *args, **kwargs)
