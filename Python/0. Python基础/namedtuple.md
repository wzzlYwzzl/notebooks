[TOC]

# namedtuple

```python
from collections import namedtuple
```

namedtuple，也即有名的元组。和它所对应的是tuple，用于存储不可修改的列表数据，访问tuple的数据是通过索引。

具体介绍namedtuple之前，先举一个简单的使用例子。

```python
from collections import namedtuple

Animal = namedtuple('Animal', 'name age type')
perry = Animal(name='perry', age=31, type='cat')

print(perry.name)
```

namedtuple是一个工厂函数，用于创建一个新的实例。这些实例既支持基于key的类似于dict的访问方式，也支持基于索引的访问。

## 简单思考使用场景

首先它有很关键的三个特征：

- dict方式的访问
- 不可变

当我们需要这两个场景时，就可以用namedtuple。
