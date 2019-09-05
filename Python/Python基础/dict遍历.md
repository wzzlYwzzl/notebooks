[TOC]

# Python dict的遍历操作

## 1. 遍历Key

```python
d = {'a':1, 'b':2, 'c':3}

# 这种方式遍历key
for key in d:
    print(key)
```

## 2. 遍历Value

```python
d = {'a':1, 'b':2, 'c':3}

for value in d.values():
    print(value)
```

## 3. 遍历item

```python
d = {'a':1, 'b':2, 'c':3}

for item in d.items():
    print(item)

'''
每个item就是一个(key,value)元组
('a',1)
('b',2)
('c',3)
'''
```

## 4. 遍历key、value

```python
d = {'a':1, 'b':2, 'c':3}

for key,value in d.items():
    print(key,value)
```
