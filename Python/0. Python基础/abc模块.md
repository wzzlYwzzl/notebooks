[TOC]

# Python抽象类相关模块abc

这个模块通常只需要使用两个对象：ABC和abstractmethod。

```python
class C(ABC): # 这里使用ABC
    @abstractmethod # 方法上使用abstractmethod
    def my_abstract_method(self, ...):
        ...
    @classmethod
    @abstractmethod # 静态方法上使用abstractmethod
    def my_abstract_classmethod(cls, ...):
        ...
    @staticmethod
    @abstractmethod
    def my_abstract_staticmethod(...):
        ...

    @property
    @abstractmethod # 属性上使用abstractmethod
    def my_abstract_property(self):
        ...
    @my_abstract_property.setter
    @abstractmethod # setter方法上使用abstractmethod
    def my_abstract_property(self, val):
        ...

    @abstractmethod
    def _get_x(self):
        ...
    @abstractmethod
    def _set_x(self, val):
        ...
    x = property(_get_x, _set_x)
```

## 参考

1. [官方文档](https://docs.python.org/zh-cn/3/library/abc.html)
