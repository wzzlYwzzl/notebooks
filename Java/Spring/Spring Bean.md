[TOC]

# Spring Bean

Spring Bean是Spring的核心概念，是Spring核心技术IOC依赖的基础。那么什么是Spring bean呢？

Spring官方文档对Bean的定义如下：

In Spring, the objects that form the backbone of your application and that are managed by the Spring IoC container are called beans. A bean is an object that is instantiated, assembled, and otherwise managed by a Spring IoC container.

**中文翻译**：在Spring中，构成应用程序主干并由Spring **IoC容器**管理的**对象**称为bean。bean是一个由Spring IoC容器**实例化、组装和管理的对象**。

在Spring Bean的定义中，涉及两个核心点：

1. IoC容器管理
2. 对象

由上面两点引出如下的问题：

1. 什么是IoC？
2. 如何做才能满足IoC要求？
3. 对象是怎样的对象才能被IoC容器管理？

## 1. IoC

IOC，Inversion of Control，控制反转。名字很奇怪，为什么叫控制反转？类的实例化、依赖的实例化、依赖的传入都交由容器来控制，不再是通过类的构造函数、属性赋值等显式依赖赋值，这样控制权的调换称之为控制反转。

IOC有助于对象之间的去耦合，对象不需要查找依赖项，甚至不需要知道依赖项在哪里定义，就能完成依赖的注入。

IOC通过IOC容器程序实现，它负责对象的实例化、依赖的管理。

## 2. Bean对象

Bean对象就是满足如下规范的Java类实例：

- 所有属性为private；
- 提供默认构造函数；
- 提供getter和setter；
- 实现serializable接口；

使用私有属性保存依赖对象，并且只能通过构造函数参数传入。

```java
public class Computer {
    private String cpu;     // CPU型号
    private int ram;        // RAM大小，单位GB

    public Computer(String cpu, int ram) {
        this.cpu = cpu;
        this.ram = ram;
    }
}
```

我们有另一个Person类依赖于Computer类，符合IoC的做法是这样：

```java
public class Person {
    private Computer computer;

    public Person(Computer computer) {
        this.computer = computer;
    }
}
```

不符合IoC的做法如下：

```java
// 直接在Person里实例化Computer类
public class Person {
    private Computer computer = new Computer("AMD", 3);
}

// 通过【非构造函数】传入依赖
public class Person {
    private Computer computer;

    public void init(Computer computer) {
        this.computer = computer;
    }
}
```

## 3. Bean对象作用域[2]

Spring框架支持六种作用域：

- singleton：在Spring IoC容器中仅存在一个Bean实例，Bean以单例方式存在，默认值

- prototype：每次从容器中调用Bean时，都返回一个新的实例，即每次调用getBean()时，相当于执行new XxxBean()

- request：每次HTTP请求都会创建一个新的Bean，该该作用域仅适用于WebApplicationContext环境

- session：同一个HTTP Session共享一个Bean，不同Session使用不同Bean，仅适用于WebApplicationContext环境

- application：单个bean的定义会被绑定到ServletContext的⽣命周期中，这个只在web-aware的Spring ApplicationContext中有效。

- websocket: 单个bean的定义会被绑定到WebSocket的⽣命周期中，这个只在web-aware的Spring ApplicationContext中有效。

六种作用域中，后面四种作用域仅在基于web的应用中使用（不必关心你所采用的是什么web应用框架），只能用在基于 web-aware 的 Spring ApplicationContext 环境。

### 3.1 singleton

singleton唯一bean实例，当一个bean的作用域为singleton，那么Spring IoC容器中只会存在一个共享的bean实例，并且所有对bean的请求，只要id与该bean定义相匹配，则只会返回bean的同一实例。这单个实例存储在单实例bean的缓存中。

注意，这里的单例不是我们设计模式中的“单例模式”中单例，这里的单例只是相对于容器而言的，同一个容器中，只有一个Bean的实例。

singleton 是单例类型，就是在创建起容器时就同时自动创建了一个bean的对象，不管你是否使用，但我们可以指定Bean节点的 lazy-init=”true” 来延迟初始化bean，这时候，只有在第一次获取bean时才会初始化bean，即第一次请求该bean时才初始化。 每次获取到的对象都是同一个对象。**注意，singleton作用域是Spring中的缺省作用域**。要在XML中将bean定义成singleton，可以这样配置：

```xml
<bean id="ServiceImpl" class="cn.csdn.service.ServiceImpl" scope="singleton">
```

也可以通过 @Scope 注解（它可以显示指定bean的作用范围。）的方式

```java
@Service
@Scope("singleton")
public class ServiceImpl{
}
```

### 3.2 prototype

prototype每次请求都会创建一个新的 bean 实例,当一个bean的作用域为 prototype，表示一个 bean 定义对应多个对象实例。prototype 作用域的 bean 会导致在每次对该 bean 请求（将其注入到另一个 bean 中，或者以程序的方式调用容器的 getBean() 方法）时都会创建一个新的 bean 实例。

prototype 是原型类型，它在我们创建容器的时候并没有实例化，而是当我们获取bean的时候才会去创建一个对象，而且我们每次获取到的对象都不是同一个对象。根据经验，对有状态的 bean 应该使用 prototype 作用域，而对无状态的 bean 则应该使用 singleton 作用域。

与其他⽣命周期不同，Spring不负责prototype bean的完整⽣命周期。容器实例化、配置或以其他⽅式组装原型对象， 然后将其交给客户端，之后就不再记录该原型实例。

因此，尽管初始化⽣命周期回调⽅法会在所有对象上被调⽤，不管⽣命周期如何，但在原型的情况下，不会调⽤配置的 销毁⽣命周期回调。客户端代码必须⾃⾏清理原型作⽤域内的对象，并释放原型bean所拥有的昂贵资源。

在 XML 中将 bean 定义成 prototype ，可以这样配置：

```xml
<bean id="account" class="com.foo.DefaultAccount" scope="prototype"/>
 或者
<bean id="account" class="com.foo.DefaultAccount" singleton="false"/>
```

通过 @Scope 注解的方式实现就不做演示了。

### 3.3 request

request每一次HTTP请求都会产生一个新的bean，该bean仅在当前HTTP request内有效,request只适用于Web程序，每一次 HTTP 请求都会产生一个新的bean，同时该bean仅在当前HTTP request内有效，当请求结束后，该对象的生命周期即告结束。 在 XML 中将 bean 定义成 request ，可以这样配置：

```xml
<bean id="loginAction" class=cn.csdn.LoginAction" scope="request"/>
```

### 3.4 session

session每一次HTTP请求都会产生一个新的bean，该bean仅在当前 HTTP session 内有效,session只适用于Web程序，session 作用域表示该针对每一次 HTTP 请求都会产生一个新的 bean，同时该 bean 仅在当前 HTTP session 内有效.与request作用域一样，可以根据需要放心的更改所创建实例的内部状态，而别的 HTTP session 中根据 userPreferences 创建的实例，将不会看到这些特定于某个 HTTP session 的状态变化。当HTTP session最终被废弃的时候，在该HTTP session作用域内的bean也会被废弃掉。

```xml
<bean id="userPreferences" class="com.foo.UserPreferences" scope="session"/>
```

### 3.5 globalSession

global session 作用域类似于标准的 HTTP session 作用域，不过仅仅在基于 portlet 的 web 应用中才有意义。Portlet 规范定义了全局 Session 的概念，它被所有构成某个 portlet web 应用的各种不同的 portle t所共享。在global session 作用域中定义的 bean 被限定于全局portlet Session的生命周期范围内。

```xml
<bean id="user" class="com.foo.Preferences "scope="globalSession"/>
```

## 4. Bean对象装配[3]

装配(wiring)，也就是依赖注入。装配过程需要显式或隐式的配置，Spring支持三种方式的配置。

1. 通过XML配置；
2. 在Java代码中配置；
3. 隐式的Bean发现机制和自动装配；

推荐方式是：3>2>1。

### 4.1 隐式Bean发现机制和自动装配

这种方式包含两部分：Bean发现和Bean装配。Bean发现通过组件扫描，Bean转配则是自动化装配。

#### 4.1.1 Bean发现

与Bean发现有关的两个注解是@Component和@Bean。

@Component告诉Spring这个类是一个组件，要为其创建一个Bean。

@Bean注解的是一个方法，告诉Spring这个方法返回一个Bean，这个方法会被Spring调用一次。

```java
package com.stalkers;

/**
 * CD唱片接口
 * Created by stalkers on 2016/11/17.
 */
public interface ICompactDisc {
    void play();
}

/*****************************/

package com.stalkers.impl;

import com.stalkers.ICompactDisc;
import org.springframework.stereotype.Component;

/**
 * Jay同名专辑
 * Created by stalkers on 2016/11/17.
 */
@Component
public class JayDisc implements ICompactDisc {

    private String title = "星晴";

    public void play() {
        System.out.println(title + ":一步两步三步四步，望着天上星星...");
    }
}

```

不过，@Component扫描默认是不开启的，需要显式的配置，才会寻找带有@Component的类，为其创建Bean。开启方式有两种：

1. 通过Java代码开启

如果CompoentScan后面没有参数的话，默认会扫描与配置类相同的包。

```java
@Configuration
@ComponentScan
public class CDPlayerConfig {
    @Bean
    public ICompactDisc disc() {
        return new JayDisc();
    }
}

/*
也可以指定扫描的基础包
*/

//方式一：包字符串
@Configuration
@ComponentScan(basePackages = {"com.stalkers.soundsystem"})
public class DiscConfig {
}

//方式二：指定一个包中的类
@Configuration
@ComponentScan(basePackageClasses = {com.stalkers.soundsystem.JayCompactDisc.class})
public class DiscConfig {
}

```

2. 通过XML配置开启

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/context
          http://www.springframework.org/schema/context/spring-context.xsd">
    <context:component-scan base-package="com.stalkers.impl"/>
</beans>
```

#### 4.1.2 Bean自动装配(Autowiring)

不同的Bean之间存在依赖，如何表示之间的依赖，如何对依赖进行注入呢？这个就需要借助于@Autowired注解。

@Autowired用来装配bean，都可以写在字段上，或者方法上。
默认情况下必须要求依赖对象必须存在，如果要允许null值，可以设置它的required属性为false，例如：@Autowired(required=false)

### 4.2 通过Java代码来装配Bean

尽管通过组件扫描和自动装配是更为推荐的方式，但是有时候却行不通，比如使用第三方组件，它们的对象中没有添加@Component和@Autowired，这个时候就需要通过JavaConfig或者XML配置。

JavaConfig与其他的Java代码又有所区别，在概念上它与应用程序中的业务逻辑和领域代码又有所不同。JavaConfig是配置相关代码，不含任何逻辑代码。通常会将JavaConfig放到单独的包中。

创建JavaConfig类的方法:

```java
@Configuration
public class CDPlayerConfig {
}
```

声明Bean:

```java
@Bean
public IMediaPlayer cdplayer() {
    return new VCDPlayer(new JayCompactDisc());
}
```

默认情况下，@Bean的Id与带有@Bean的方法名一样。当然也可以通过@Bean的name属性指定额外的方法名。

但是上面的做法初始化个VCDPlayer都需要new一个JayCompactDisc对象，如果有其他对象也需要JayCompactDisc，那么上面的代码可以如下优化：

```java
@Bean
public IMediaPlayer cdplayer() {
    return new VCDPlayer(disc());
}

@Bean
public ICompactDisc disc() {
    return new JayCompactDisc();
}
```

单独抽出disc()方法，在其方法上加上Bean注解，Spring上加@Bean注解的都是默认单例模式，不管disc()被多个方法调用，其disc()都是同一个实例。

### 4.3 XML装配Bean

在XML文件中定义Bean，同时组装bean。

#### 4.3.1 XML基础格式

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

</beans>
```

在使用xml的时候，需要在配置文件顶部声明多个xml模式（XML Schema Definition xsd）文件

对于我们需要配置bean的则在spring-beans模式中。

#### 4.3.2 构造器注入初始化Bean

构造器注入的方式也有两种写法：

1. 通过XML的constructor-arg元素来注入依赖

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="jayCompactDisc" class="com.stalkers.soundsystem.JayCompactDisc"></bean>
    <bean id="cdPlayer" class="com.stalkers.soundsystem.VCDPlayer">
        <constructor-arg ref="jayCompactDisc"/>
    </bean>
</beans>
```

2. 通过Spring 3.0中引入的c-命名空间

首先需要引入：xmlns:c="http://www.springframework.org/schema/c"

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:c="http://www.springframework.org/schema/c"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="jayCompactDisc" class="com.stalkers.soundsystem.JayCompactDisc"></bean>
    <bean id="cdPlayer" class="com.stalkers.soundsystem.VCDPlayer" c:cd-ref="jayCompactDisc">
    </bean>
</beans>
```

c:cd-ref="jayCompactDisc"格式说明：

- c 代表命名空间前缀
- cd 代表VCDPlayer类的构造器参数名。当然我们也可以使用参数在整个参数列表的位置 c:_0-ref，使用下划线因为参数不能以数字开头，所以加下划线。
- -ref 代表注入bean引用
- jayCompactDisc 要注入的bean的id

上面的写法是装配一个Bean对象的引用，但是有时我们也需要**装配一个字面量值**，比如int、String等类型，此时的写法如下：

```java
public class VaeCompactDisc implements ICompactDisc {
    private String title;

    public VaeCompactDisc(String title) {
        this.title = title;
    }

    public void play() {
        System.out.println("大家好，我是Vae，下面这首：" + title + "献给大家的");
    }
}
```

元素表示法如下：

```xml
<bean id="cdPlayer" class="com.stalkers.soundsystem.VCDPlayer" c:_0-ref="vaeCompactDisc">
</bean>
<bean id="vaeCompactDisc" class="com.stalkers.soundsystem.VaeCompactDisc">
    <constructor-arg value="浅唱"></constructor-arg>
</bean>
```

命名空间表示法如下：

```xml
<bean id="cdPlayer" class="com.stalkers.soundsystem.VCDPlayer" c:_0-ref="vaeCompactDisc">
</bean>
<bean id="vaeCompactDisc" class="com.stalkers.soundsystem.VaeCompactDisc" c:title="城府">
</bean>
```

装配集合类型的数据：

```java
public class VaeCompactDisc implements ICompactDisc {
    private String title;

    private List<String> tracks;

    public VaeCompactDisc(String title, List<String> tracks) {
        this.title = title;
        this.tracks = tracks;
    }

    public void play() {
        System.out.println("大家好，我是Vae，下面这专辑：" + title + "献给大家的");
        for (String s : tracks) {
            System.out.println(s);
        }
    }
}
```

c-命名空间的方式无法使用装配集合的功能，只能通过使用constructor-arg。

```xml
<bean id="cdPlayer" class="com.stalkers.soundsystem.VCDPlayer" c:_0-ref="vaeCompactDisc">
</bean>
<bean id="vaeCompactDisc" class="com.stalkers.soundsystem.VaeCompactDisc">
    <constructor-arg name="title" value="自定义"></constructor-arg>
    <constructor-arg name="tracks">
        <list>
            <value>有何不可</value>
            <value>多余的解释</value>
        </list>
    </constructor-arg>
</bean>
```

#### 4.3.3 使用属性setter方法注入

```java
public class CDPlayer implements IMediaPlayer {

    private ICompactDisc cd;

    @Autowired
    public void setCd(ICompactDisc cd) {
        this.cd = cd;
    }

    public CDPlayer(ICompactDisc cd) {
        this.cd = cd;
    }

    public void play() {
        System.out.println("cd Play:");
        cd.play();
    }
}
```

通过XML元素的方式配置方法如下：

```xml
<bean id="cdPlayer" class="com.stalkers.soundsystem.VCDPlayer">
    <property name="cd" ref="jayCompactDisc"></property>
</bean>
```

通过命名空间的方式如下：p-命名空间

需要引入：xmlns:p="http://www.springframework.org/schema/p"

```xml
<bean id="cdPlayer" class="com.stalkers.soundsystem.VCDPlayer" p:cd-ref="vaeCompactDisc">
```

p:cd-ref="vaeCompactDisc"格式说明：

- p-:命名空间的前缀
- cd:属性名称
- -ref:注入bean引用
- vaeCompactDisc：所注入的bean的id

### 4.4 多种方式混合

在Spring应用中，我们可以同时使用自动化和显示配置。
如果一个JavaConfig配置太臃肿，我们可以把其进行拆分，然后使用@Import将拆分的类进行组合。
如果希望在JavaConfig里引用xml配置。则可以使用@ImportResource

## 参考

1. [spring bean是什么](https://www.awaimai.com/2596.html)
2. [SpringBean 工作原理详解](https://www.cnblogs.com/yoci/p/10642553.html)
3. [Spring Bean详细讲解 什么是Bean?](https://blog.csdn.net/weixin_43277643/article/details/84253237)
