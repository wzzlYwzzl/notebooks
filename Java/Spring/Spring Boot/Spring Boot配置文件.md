[TOC]

# Spring Boot配置文件

Spring Boot配置相关的内容，从两个维度介绍：

- 配置存放到哪里
- 如何获取配置内容

## 1. Spring Boot的配置内容存放位置

配置可以放到三种地方：

- 默认全局配置文件：application.properties和application.yaml
- 自定义配置文件
- 配置类

### 1.1 全局默认配置文件

Spring Boot默认会从application.properties和application.yaml两个文件中读取配置项的。**注意**：配置文件必须要放到/src/main/resource目录中。

这两个文件如果同时存在，那么properties文件优先级更高。

下面给出一个比较完整的application.properties配置文件的完整例子来介绍一些细节使用方式。

定义一个存放配置的类：

```java

@Component
public class Pet{
    private String type;
    private String name;

    /*
     * 省略getter方法和setter方法
     */
}

@Component
@ConfigurationProperties(prefix= "person")
public class Person{
    private int id;
    private String name;
    private List hobby; //list类型
    private String[] family; //数组类型
    private Map map; //map类型
    private Pet pet; //自定义类型

    /*
     * 省略getter方法和setter方法
     */
}

```

在application.properties中写入对应的配置：

```txt
person.id = 1
person.name = tom
person.hobby = play,read,sleep
person.family = father,mother
person.map.k1 = v1
person.map.k2 = v2
person.pet.type = dog
person.pet.name = kity
```

### 1.2 自定义配置文件

通过全局的默认配置文件，可以很方便地添加配置，无需为配置文件管理操心。但是，有时我们可能真的需要创建自己的配置文件。

如何导入自定义配置文件呢？

有两种方式：

- @PropertySource
- @ImportResource

**@PropertySource**

假设自定义配置文件test.properties，文件内容如下：

```txt
test.id=123
test.name=test
```

与其对应的配置类如下：

```java

@Component
@PropertySource("classpath:test.properties")
@ConfigurationProperties(prefix="test")
public class MyProperties {
    private id;
    private String name;

    /*
     * 省略getter方法和setter方法
     */
}
```

**@ImportResource**

传统的Spring配置基于XML文件，Spring Boot则默认不再使用XML文件配置项目，而且XML配置文件不会加载到Spring容器中。如果希望将外部的XML配置加载到程序中，那么可以使用@ImportResource注解加载配置。

### 1.3 自定义配置类

@ImportResource方法引入自定义XML配置的方式只在特殊场景使用，在Spring Boot中，根据“约定大于配置”的指导原则，建议使用配置类的方式。

与配置类有关的两个注解：@Configuration和@Bean。

```java
@Configuration
public class MyConfig {
    @Bean
    public MyService myService() {
        return new MyServcie();
    }
}
```

Spring Boot会自动扫描@Configuration注解声明的配置类，内部使用@Bean注解的方法的返回值对象会作为一个组件添加到Spring容器中。该组件的id就是该方法的名称。

## 2. 如何获取配置文件的内容

如果是直接注入变量，那么就两种注入方式：@ConfigurationProperties和@Value，这两种方式也是Spring Boot和Spring提供的标准用法。

### 2.1 两种方式的对比

| 对比点 | @ConfigurationProperties | @Value |
| - | - | - |
| 底层框架 | Spring Boot | Spring |
| 功能 | 批量注入配置文件的属性 | 单个注入 |
| setter方法 | 需要 | 不需要 |
| 复杂类型属性注入 | 支持 | 不支持 |
| 松散绑定 | 支持 | 不支持 |
| JSR303数据校验 | 支持 | 不支持 |
| SpEL表达式 | 不支持 | 支持 |


**底层框架：**
@ConfigurationProperties注解是Spring Boot框架自带，@Value是Spring框架支持的，Spring Boot对Spring进行了默认支持。

**属性setter方法：**
@ConfigurationProperties需要为每个属性设置setter方法，这样才能将配置文件中的属性一一匹配并注入到对应Bean的属性中。如果配置文件中没有配置对应的属性值，那么Bean中对应的属性就会设置为空。

@Value不需要设置setter方法，该注解会通过表达式读取配置文件中的属性值，然后注入到下方Bean的属性上。如果读取的配置文件属性为空，进行属性注入时，程序就会自动报错。

**复杂类型注入：**
@ConfigurationProperties可以导入复杂对象，但是@Value只能注入基本类型的属性。

**松散绑定：**
所谓松散绑定，就是多种配置格式都可以对应同一个变量名称。

比如：
```txt
person.firstName = james
person.first-name = james
person.first_name = james
person.FIRST_NAME = james
```

上面这种松散绑定@ConfigurationProperties都可以对应firstName属性，但是@Value不会无法通过上面注入。

**JSR303校验：**
@ConfigurationProperties在注入属性值时，支持JSR303校验。使用方法为在类上添加@Validated注解，然后在相应属性上添加相应校验规则对应的注解。

比如：

```java
@Component
@ConfigurationProperties
@Validated
public class Example {
    @Email
    private String email;

    public void setEmail(String value){
        this.email = value
    }
}
```

**两种方式的使用场景建议：**

- 如果是个别的配置，那么可以使用@Value；
- 如果针对某个类批量注入属性配置，那么推荐使用@ConfigurationProperties；