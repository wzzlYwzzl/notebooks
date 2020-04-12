[TOC]

# Java对象序列化

## 序列化与反序列化

- 把Java对象转换为字节序列的过程称为序列化。
- 把字节序列解析为Java对象的过程称为反序列化。

Java对象的序列化有两个用处：

- 便于把对象永久存储；
- 便于网络传输Java对象；

## JDK类库中的序列化反序列化API

```java
/*
 序列化是用到的输出流，调用它的writeObject(Object obj)方法将对象进行序列化
*/
java.io.ObjectOutputStream

/*
 调用它的readObject()方法从一个源中读取字节流进行反序列化得到一个对象
*/
java.io.ObjectInputStream
```

一个Java对象要想能够被序列化和反序列化，它对应的类必须实现Serializable或者Externalizable这两个接口。

```java
/*
 Serializable接口的定义，是个空接口，可以理解为开关，由写程序的人控制哪个对象允许序列化。
*/
public interface Serializable{}

public interface Externalizable extends Serializable {
    void writeExternal(ObjectOutput out) throws IOException;
    void readExternal(ObjectInput in) throws IOException,ClassNotFoundException;
}
```

实现Serializable接口的对象，使用默认的序列化和反序列化方法。实现Externalizable接口的对象，自定义序列化和反序列化方法。

## 序列化与反序列化实例

```java
import java.io.Serializable

/*
 要序列化的对象
*/
public class Person implements Serializable {
    private static final long serialVersionUID = -5809782578272943999L;
    private int age;
    private String name;
    private String sex;

    public int getAge() {
        return age;
    }

    public String getName() {
        return name;
    }

    public String getSex() {
        return sex;
    }

    public void setAge(int age) {
        this.age = age
    }

    public void setName(String name) {
        this.name = name
    }

    public void setSex(String sex) {
        this.sex = sex
    }
}

public class Test {
    public static void main(String[] args) throws Exception{

    }

    /**
    测试序列化方法
    **/
    private static void SerializePersion() throws FileNotFoundException, IOException {
        Person person = new Person();
        person.setName("xiaoming");
        person.setAge(18);
        person.setSex("male");

        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(new File("./person.txt")));
        out.writeObject(person);
        out.close();
    }

    /**
    测试反序列化方法
    **/
    private static Person DeserializePerson() throws Exception, IOException {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(new File("./person.txt")));
        Person person = (Person)in.readObject();
        return person;
    }
}
```

## serialVersionUID的作用

序列化版本号，凡是实现了Serializable接口的类都需要一个表示序列化版本号的静态成员。

那么这个序列化版本号到底有什么用呢？

先通过一个例子说明它的作用：

上面的Person，我们将其序列化到了person.txt文件中，后面我们修改了Person类，在其中添加了一个新的成员height，对于新的类，我们调用反序列化方法，如果我们没有指定serialVersionUID，那么反序列化时就会抛出InvalidClassException异常。因为这两个类不兼容了，出于安全考虑，程序就抛出错误。

为什么会抛出错误呢？
因为如果不指定serialVersionUID，那么java编译器会自动为这个class进行一个摘要算法，类似于指纹算法，得到一个UID，只要class发生一个空格的变化，就会得到一个不一样的UID。

如何避免这种后期新添加字段反序列化时出现错误呢？
手动指定serialVersionUID。这样，如果希望新旧版本的class能够序列化兼容的话，就可以指定相同的UID，如果不希望二者兼容，那么就可以指定不同的UID。
