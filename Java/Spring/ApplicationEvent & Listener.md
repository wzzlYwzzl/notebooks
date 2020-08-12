[TOC]

# Spring ApplicationEvent & Listener

ApplicationEvent 以及 Listener 是 Spring 为我们提供的一个事件监听、订阅的实现，内部实现原理是观察者设计模式，设计初衷也是为了系统业务逻辑之间的解耦，提高可扩展性以及可维护性。事件发布者并不需要考虑谁去监听，监听具体的实现内容是什么，发布者的工作只是为了发布事件而已。

## 1. 使用方法

Spring 提供的事件发布、订阅机制的使用方式总的来说分为三步：

1. 创建事件
2. 创建 Listener
3. 发布事件

下面就按照上面的三个步骤介绍其使用过程。

### 1.1 创建事件

所谓事件，就是一个 pojo，没有其他的约束。但是，我们在实际使用过程中，创建事件时，我们都会继承一个类`ApplicationEvent`，这个类中添加了一些约定的属性。

```java
public class HelloEvent extends ApplicationEvent {

    private String name;

    /**
    * 这里的source通常用来存储事件中携带的其他数据，实际上我们也可以在
    * 自定义的事件中添加自己的属性。
    **/
    public HelloEvent(Object source, String name) {
        super(source);
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

### 1.2 创建事件 Listener

创建 Listener 主要有三种方式：

1. 实现`ApplicationListener<T>`接口；
2. 实现`SmartApplicationListener`接口；
3. 通过`@EventListener`注解一个方法；

下面分别介绍三种方式的使用方法。

#### 1.2.1 ApplicationListener\<T>

```java
@Component // 声明为组件
public class HelloEventListener implements ApplicationListener<HelloEvent> {
    private static final Logger logger = LoggerFactory.getLogger(HelloEventListener.class);

    // 这个方法用来处理指定类型的事件
    @Override
    public void onApplicationEvent(HelloEvent event) {
        logger.info("receive {} say hello!",event.getName());
    }
}
```

#### 1.2.2 SmartApplicationListener

上面使用`ApplicationListener`的方式创建的事件订阅者之间的顺序是随机的，无法保证不同的 Listener 的接受顺序。这个时候，我们可以使用`SmartApplicationListener`接口来创建 Listener。

`SmartApplicationListener`接口继承了`ApplicationListener`和`Ordered`两个接口，所以需要实现四个方法：

```java
{
    // 事件的类型是否匹配
    public boolean supportsEventType(Class<? extends ApplicationEvent> aClass);

    // 事件的source数据的类型是否匹配
    public boolean supportsSourceType(Class<?> aClass);

    // 处理事件逻辑，当上面两个都返回true时，调用这个方法
    public void onApplicationEvent(ApplicationEvent applicationEvent);

    // 事件优先级，越小表示优先级越高
    public int getOrder();
}
```

#### 1.2.3 @EventListener

这个是 Spring 4.2 之后引入的更为方便的创建 Listener 的方式。通过它我们可以实现前面两种方式的功能。

我们现在说明它是如何替换前面的两个接口的功能的。

1. 替换`ApplicationListener`接口

创建一个函数，这个函数的参数类型就是要 Listen 的事件类型，然后在这个函数上添加这个@EventListener 注解即可。

```java
@Component
class Test {

    @EventListener
    public void onMyEventListener(HelloEvent event) {
        // do something
    }
}
```

2. 如何实现对事件的过滤

在`SmartApplicationListener`中有两个函数：supportsEventType 和 supportsSourceType 来对事件进行过滤。@EventListener 注解则是两个属性可以实现这个功能：classes 和 condition。

```java
@Component
class Test {

    @EventListener(classes=HelloEvent.class, condition="SpEL表达式")
    public void onMyEventListener(HelloEvent event) {
        // do something
    }
}
```

3. 如何指定 Listener 的顺序

方法就是在@EventListener 添加方法上再添加@Order 注解。

```java
@Component
class Test {

    @Order(1)
    @EventListener(classes=HelloEvent.class, condition="SpEL表达式")
    public void onMyEventListener(HelloEvent event) {
        // do something
    }
}
```

### 1.3 发布事件

发布事件的方法很简单，就是通过 ApplicationContext 的 publishEvent 方法。

```java
applicationContext.publishEvent(new HelloEvent(this,"lgb"));
```

## 2. 异步监听

按照前面的方法发布事件，那么执行发布事件是阻塞的，需要等到事件相关的 Listener 处理完成之后，publishEvent方法才能返回。有时我们不需要等待他们的返回，怎么办呢？

方法就是使用`@Async`实现异步监听。

具体做法就是将`@Async`注解添加到具体处理事件的方法上。注意，要想激活异步相关的注解，需要在配置类上添加`@EnableAsync`注解。`@Async`注解底层使用的是线程池，所以，我们也可以配置线程池。

配置线程池做法：

```java
package com.yuqiyu.chapter27;

import org.springframework.aop.interceptor.AsyncUncaughtExceptionHandler;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class ListenerAsyncConfiguration implements AsyncConfigurer
{
    /**
     * 获取异步线程池执行对象
     * @return
     */
    @Override
    public Executor getAsyncExecutor() {
        //使用Spring内置线程池任务对象
        ThreadPoolTaskExecutor taskExecutor = new ThreadPoolTaskExecutor();
        //设置线程池参数
        taskExecutor.setCorePoolSize(5);
        taskExecutor.setMaxPoolSize(10);
        taskExecutor.setQueueCapacity(25);
        taskExecutor.initialize();
        return taskExecutor;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return null;
    }
}
```

## 3. Spring内置事件

ContextClosedEvent 、ContextRefreshedEvent 、ContextStartedEvent 、ContextStoppedEvent 、RequestHandleEvent。

### 3.1 ContextRefreshedEvent

在IOC的容器的启动过程，当所有的bean都已经处理完成之后，spring ioc容器会发布此事件。

ContextRefreshedEvent 事件会在Spring容器初始化完成会触发该事件。我们在实际工作也可以能会监听该事件去做一些事情，但是有时候使用不当也会带来一些问题。

1. 防止重复触发

在web 项目中（spring mvc），系统会存在两个容器，一个是root application context ,另一个就是我们自己的 projectName-servlet context（作为root application context的子容器）。

主要因为对于web应用会出现父子容器，这样就会触发两次，那么如何避免呢？

下面给出一种简单的处理方法：

```java
@Component
public class TestTask implements ApplicationListener<ContextRefreshedEvent> {
    private volatile AtomicBoolean isInit=new AtomicBoolean(false);
    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        //防止重复触发
        if(!isInit.compareAndSet(false,true)) {
            return;
        }
        start();
    }

    private void start() {
        //开启任务
        System.out.println("****-------------------init---------------******");
    }
}
```
