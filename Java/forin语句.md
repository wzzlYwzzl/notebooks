[TOC]

# Java中的for-in语句

for-in是JDK5中引入的一个新特性，为的就是语法上更为简洁的使用迭代器。

在for-in引入之前，如果使用迭代器，那么用法如下：

```java
List<String> list = new ArrayList<String>();
list.add("a");
list.add("b");
list.add("c");

Iterator<String> it = list.iterator();
while (it.hasNext()) {
    System.out.println(iterator.next());
}
```

如果使用for-in的话，就会化简成如下的形式：

```java
for (String item : list){
    System.out.println(item);
}
```

## 如何让自定义对象支持for-in

1. 需要自定义对象实现Iterable\<E>接口，这个接口就一个iterator方法。

```java
interface Iterable<E> {
    Iterator<E> iterator();
}
```

2. 由于iterator方法返回的对象是Iterator接口，所以还要实现Iterator接口

```java
interface Iterator<E> {
    boolean hasNext();
    E next();
    void remove();
}
```
