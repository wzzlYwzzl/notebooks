[TOC]

# Python对象序列化与反序列化

下面内容翻译自[pickle官方文档](https://docs.python.org/3/library/pickle.html)。

pickle模块实现了对Python对象的序列和反序列化的二进制协议。pickling过程就是将Python对象层级地转化为二进制流的过程，unpickling则是相反的过程。

```txt
注意：

pickle模块是不安全的，所以只unpickle信任的数据。

构建恶意的pickle数据是可能的，它们会在unpickle时执行任意的代码。所以不要unpickle来源不信任的数据，或者可能被篡改的数据。

可以考虑用hmac对数据进行签名以确保它没有被篡改。

如果处理不信任的数据，可以考虑使用json这种序列化格式。

```

## 1. 与Python其他模块的关系

### 1.1 与marshal比较

Python有一个更加原始的序列化模块叫marshal，但是pickle应该总是作为优先的方式来序列化Python对象。marshal的存在主要是用于支持Python的.pyc文件。

pickle和marshal主要区别在于：

- pickle模块会记录已经序列化的对象，后面指向同一对象的引用不会在序列化。但是marshal不是。

- marshal不能用于序列化自定义类和它们的实例。pickle可以透明地保存和还原类实例。但是，这些类的定义必须要importable，同时在对象stored时，要在同一个module。

- marshal序列化的格式无法保证不同python版本之间兼容。因为它的主要工作是支持pyc文件，python的实现有权利改变序列化方式而不向前支持。pickle的序列化格式通过提供兼容的pickle协议而向前支持。

### 1.2 与json比较

二者之间根本性的不同在于：

- json是文本序列化格式，pickle是二进制序列化格式；
- json可是人可读，但是pickle不可读；
- json可以跨语言，但是pickle不可以；
- json，默认只能表示Python内置类型的一部分，也不支持自定义类。pickle则可以支持绝大部分的Python类型。
- 不像pickle，序列化不可信的json不会导致创建任意代码执行漏洞。

## 2. 数据流格式

pickle使用的数据格式是Python特有的。好处就是不像Json或XDR有额外的限制，同时也意味着其他语言不能构建pickle导出的对象。

默认，pickle的数据格式是相对紧凑的二进制表示，如果你需要优化大小特性，可以有效地压缩pickled数据。

pickletools模块包含一些分析pickle产生的数据流的工具。pickletools源码中包含了大量关于pickle协议使用的机器码的注解。

目前，有6中不同的协议pickle可以使用。越高的协议，那么Python版本就要越新。

- **协议版本0**是原始的人可读的协议，兼容更早期的Python版本。

- **协议版本1**是老的二进制格式，也兼容早期的Python版本。

- **协议版本2**在Python2.3引入。它提供了更为有效的新式类的封装。

- **协议版本3**是在Python3中添加的。它支持bytes对象，且不能被Python 2.x版本unpickle。

- **协议版本4**在Python4中添加的，添加了对大对象的支持，可以封装更多类型的对象，且优化了一些数据格式。从Python 3.8开始是默认的协议。

- **协议版本5**是在Python 3.8中添加的，添加了对out-of-band数据的支持，同时提高了in-band数据的速度。

```txt
注意：序列化是一个比持久化更原始的概念，尽管pickle模块读取和写入文件中的对象，但是它不处理命名持久化对象的问题，也不处理并发访问持久化对象的问题。pickle可以将一个复杂对象转换为字节流，也可以吧字节流转换为一个对象。或许处理这些字节流的明显做法是写入文件，但是也可以在网络上传输这些内容，或者写入到数据库。shelve模块就是一个简单的接口，帮助把对象写入到数据库风格的文件中。
```

## 3. 哪些对象可以pickled或unpickled

- None, True, False
- int，float，复数
- tuples、list、set、只包含可以pickled对象的dict
- 定义在module顶层的函数，用def定义的，不能是lambda函数
- 内置的定义在module顶层的函数
- 定义在module顶层的class
- 这种类型的class的实例：这些class的__dict__可以pickle，或者调用__getstate__()方法返回的结果可以pickled。

## 参考

1. [pickle官方文档](https://docs.python.org/3/library/pickle.html)
