[TOC]

# Python装饰器

## 参考

[Python3装饰器全解](https://www.cnblogs.com/whyaza/p/9505205.html)

## 被修饰函数和装饰器都不带参数

```python
import time
def showtime(func):
    def wrapper():#这里是否带参数取决于被修饰的函数是否带参数
        start_time = time.time()
        func()
        end_time = time.time()
        print('spend is {}'.format(end_time - start_time))

    return wrapper

@showtime  #foo = showtime(foo)
def foo():
    print('foo..')
    time.sleep(3)

@showtime #doo = showtime(doo)
def doo():
    print('doo..')
    time.sleep(2)

foo()
doo()
```

## 装饰器不带参数被修饰函数带参数

```python
import time
def showtime(func):
    def wrapper(a, b):#被装饰的函数带的参数类型
        start_time = time.time()
        func(a,b)
        end_time = time.time()
        print('spend is {}'.format(end_time - start_time))

    return wrapper

@showtime #add = showtime(add)
def add(a, b):
    print(a+b)
    time.sleep(1)

@showtime #sub = showtime(sub)
def sub(a,b):
    print(a-b)
    time.sleep(1)

add(5,4)
sub(3,2)
```

## 装饰器带参数

实际是对原有装饰器的一个函数的封装,并返回一个装饰器(一个含有参数的闭包函数)。

```python
import time
def time_logger(flag = 0):# 最外层又多了一个封装
    def showtime(func):# 从这里开始，是原来的不带参数装饰器
        def wrapper(a, b):
            start_time = time.time()
            func(a,b)
            end_time = time.time()
            print('spend is {}'.format(end_time - start_time))

            if flag:
                print('将此操作保留至日志')

        return wrapper

    return showtime

@time_logger(2)  #得到闭包函数showtime,add = showtime(add)
def add(a, b):
    print(a+b)
    time.sleep(1)

add(3,4)
```
