[TOC]

# __str__ 和 __repr__

__str__函数是在执行print函数输出时调用的函数。
__repr__函数是直接输入类对象打印的信息。

举例说明：

```python
class A:
    def __init__(self):
        self.info = 'this is class a'

class TestStr(A):
    def __str__(self):
        return self.info

class TestRepr(A):
    def __repr__(self):
        return self.info
```

```shell
>>> t = TestRepr()
>>> t
# 这里的输出就是由__repr__函数决定的

>>> t2 = TestStr()
>>> print(t2)
# 这里的输出是由__str__函数决定的
```

通过上面的例子，我们应该能明白，__repr__函数是面向程序员，__str__是面向用户的。
