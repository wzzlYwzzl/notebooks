[TOC]

# Python读取Yaml文件

## 1. Yaml文件规则

- 大小写敏感；
- 与Python类似，通过缩进来表示层级关系，缩进只允许使用空格，不允许使用Tag；
- 缩进的空格数目多少没有关系，只要保持同一级缩进数目相同即可；
- 注释使用“#”。

## 2. Yaml支持的数据结构

1. key:value键值对

```yaml
user: admin
password: 123456
```

2. 字典嵌套

```yaml
test:
    user: admin
    password: 123456
```

3. list

```yaml
test:
    - abc
    - efg
    - hig
```

4. scalars（纯量）

单个的不可再分的值。比如字符串、布尔值、整数、浮点数、Null、时间、日期。

```yaml
testfloat: 12.30

testbool: true

testnone: ~

testtime: 2001-12-14t21:59:43.10-05:00
```

5. 强制类型转换

通过两个叹号来对类型强制转换。

```yaml
test: !!str 123
test: !!str true
```

## 3. Python读取Yaml文件

Yaml测试内容如下：

```yaml

test1: 123

dict:
    a: 1
    b: abc
    c: true

test2:
    - a
    - b
    - c

test3: 1.23

test4: !!str 4.56

test5: !!str true

```

上面的内容放置到一个文件中，通过如下方式读取：

```python
with open(yaml_file, 'r', encoding='utf8') as f:
    yaml_data = yaml.load(f, yaml.FullLoader)
    print(yaml_data)

# 程序得到如下内容：
{'test1': 123, 'dict': {'a': 1, 'b': 'abc', 'c': True}, 'test2': ['a', 'b', 'c'], 'test3': 1.23, 'test4': '4.56', 'test5': 'true'}

```
