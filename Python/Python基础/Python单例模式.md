[TOC]

# Python单例模式

python单例模式有以下几种方式：

1. 通过模块调用
2. 使用__new__方法
3. 使用装饰器
4. 使用元类

## 1. 通过模块的import实现单实例

这种方式类似于全局变量的定义方式。由于一个模块在系统中只有一个实例，所以通过模块导入多次时，得到的仍是一个实例。

用法举例：

```python

# 假设单实例模块为test.py
class TestClass:
    pass

export_single = TestClass()

#在使用模块中，如下方式使用
from test import export_single
```

## 2. 通过___new__的方式

__new__方法：在创建实例是调用的方法。
__init__方法：在初始化实例是调用的方法。

```python
class Singleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance


a = Singleton()
b = Singleton()
print(id(a) == id(b))
```

## 3. 通过装饰器

Python装饰器是一个函数，经常用在有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限验证等。关于Python装饰器的内容，有专门的一个“markdown”来介绍这个知识点。

```python
from functools import wraps


def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class Singleton(object):
    def foo(self):
        pass


a = Singleton()
b = Singleton()
print(id(a) == id(b))
```

## 4. 通过元类

关于什么是元类，可以参考“Python元类”的markdown文件。

```python
class SingletonMeta(type):
    __instance = None
    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwargs)
        return cls.__instance


class MyClass(metaclass=SingletonMeta):
    def foo(self):
        pass


a = MyClass()
b = MyClass()
print(id(a) == id(b))
```

## 5. 通过类创建单实例

这个方法核心就是通过静态方法获取单实例。

```python
import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance


def task(arg):
    obj = Singleton.instance() # 获取单实例的方法
    print("Task {}".format(arg), id(obj))


for i in range(10):
    t = threading.Thread(target=task, args=[i,])
    t.start()
```
