[TOC]

# Python自带队列

## LILO队列

这个队列就是数据结构中我们所说的基础队列。

```python
from queue import Queue #LILO队列
q = Queue() #创建队列对象
q.put(0)    #在队列尾部插入元素
q.put(1)
q.put(2)
print('LILO队列',q.queue)  #查看队列中的所有元素
print(q.get())  #返回并删除队列头部元素
print(q.queue)

```

## LIFO队列

这个队列对应于数据结构的栈。

```python
from queue import LifoQueue #LIFO队列
lifoQueue = LifoQueue()
lifoQueue.put(1)
lifoQueue.put(2)
lifoQueue.put(3)
print('LIFO队列',lifoQueue.queue)
lifoQueue.get() #返回并删除队列尾部元素
lifoQueue.get()
print(lifoQueue.queue)
```

## PriorityQueue优先队列

[Python优先级队列](https://zhuanlan.zhihu.com/p/37637660)

```python

from queue import PriorityQueue #优先队列
priorityQueue = PriorityQueue() #创建优先队列对象
priorityQueue.put(3)    #插入元素
priorityQueue.put(78)   #插入元素
priorityQueue.put(100)  #插入元素
print(priorityQueue.queue)  #查看优先级队列中的所有元素
priorityQueue.put(1)    #插入元素
priorityQueue.put(2)    #插入元素
print('优先级队列:',priorityQueue.queue)  #查看优先级队列中的所有元素
priorityQueue.get() #返回并删除优先级最低的元素
print('删除后剩余元素',priorityQueue.queue)
priorityQueue.get() #返回并删除优先级最低的元素
print('删除后剩余元素',priorityQueue.queue)  #删除后剩余元素
priorityQueue.get() #返回并删除优先级最低的元素
print('删除后剩余元素',priorityQueue.queue)  #删除后剩余元素
priorityQueue.get() #返回并删除优先级最低的元素
print('删除后剩余元素',priorityQueue.queue)  #删除后剩余元素
priorityQueue.get() #返回并删除优先级最低的元素
print('全部被删除后:',priorityQueue.queue)  #查看优先级队列中的所有元素

```

## deque 双端队列

```python

from collections import deque   #双端队列
dequeQueue = deque(['Eric','John','Smith'])
print(dequeQueue)
dequeQueue.append('Tom')    #在右侧插入新元素
dequeQueue.appendleft('Terry')  #在左侧插入新元素
print(dequeQueue)
dequeQueue.rotate(2)    #循环右移2次
print('循环右移2次后的队列',dequeQueue)
dequeQueue.popleft()    #返回并删除队列最左端元素
print('删除最左端元素后的队列：',dequeQueue)
dequeQueue.pop()    #返回并删除队列最右端元素
print('删除最右端元素后的队列：',dequeQueue)
```