[TOC]

# Spring AOP

## 入门案例A

### 1. pom.xml配置

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>Garvey</groupId>
  <artifactId>Spring-Learn</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <name>Spring-AOP</name>
  
  <dependencies>
        <!-- spring-ioc: 以后使用spring其他功能，都必须先导入ioc相关依赖 -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>5.0.2.RELEASE</version>
        </dependency>

        <!-- spring-aop spring自身aop编程包 -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-aop</artifactId>
            <version>5.0.2.RELEASE</version>
        </dependency>
        <!-- spring依赖的第三方工具包(提供切入点表达式语法) -->
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
            <version>1.8.7</version>
        </dependency>
    </dependencies>
</project>
```

### 2. Service接口

这个接口表示的是正常的业务逻辑代码。

```java
package garvey;

public interface GarveyService {

    void save();
    void delete();
    void update();
}
```

### 3. 业务代码的实现

```java
package garvey;

public class GarveyServiceImpl implements GarveyService {
    @Override
    public void save() {
        System.out.println("新增");
    }

    @Override
    public void delete() {
        System.out.println("删除");
    }

    @Override
    public void update() {
        System.out.println("修改");
    }
}
```

### 4. 定义切面逻辑

```java
package garvey;

public class LogAspect {
    /**
     * 通知方法（插入到目标方法的前面）
     */
    public void writeLog(){
        System.out.println("before=======");
    }
}
```

### 5. 切面配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!-- 1.创建目标对象 -->
    <bean id="garveyService" class="garvey.GarveyServiceImpl"/>

    <!-- 2.创建切面对象 -->
    <bean id="logAspect" class="garvey.LogAspect"/>

    <!-- 3.切面配置 -->
    <aop:config>
        <!-- 切面配置 = 通知（advice）+切入点（pointcut）-->
        <!--
            ref： 引用切面类对象
         -->
        <aop:aspect ref="logAspect">
            <!-- 定义切入点 -->
            <!--
                id: 定义切入点的别名
                expression： 切入点表达式（用于定义需要切入的方法）
             -->
            <aop:pointcut id="pt" expression="execution(* garvey.GarveyServiceImpl.*(..))"/>

            <!-- 定义通知 -->
            <!--
               method: 使用切面类的哪个方法作为通知方法
               pointcut-ref： 关联切入点
             -->
            <!-- 前置通知 -->
            <aop:before method="writeLog" pointcut-ref="pt"/>
        </aop:aspect>
    </aop:config>
</beans>
```

### 6. main方法

```java
package garvey;

import garvey.GarveyService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

//测试AOP
public class App {

    public static void main(String[] args) {
        ApplicationContext ac = new ClassPathXmlApplicationContext("classpath:application.xml");
        GarveyService lemonService = (GarveyService) ac.getBean("garveyService");
        System.out.println("代理对象"+lemonService.getClass());
        lemonService.save();
        lemonService.delete();
        lemonService.update();
    }

}
```

## 入门案例B
