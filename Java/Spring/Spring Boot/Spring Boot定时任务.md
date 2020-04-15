[TOC]

# Spring Boot定时任务

## 1. 代码举例

### 1.1 基本操作

1. pom.xml中添加依赖

官网的例子中，添加了awaitility依赖，是因为它在测试代码中用到了异步编程，所以加入了这个依赖，如果不需要异步测试，是不需要添加的。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.2.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.example</groupId>
    <artifactId>scheduling-tasks</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>scheduling-tasks</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.awaitility</groupId>
            <artifactId>awaitility</artifactId>
            <version>3.1.2</version>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

### 1.2 cron表达式

corn表达式格式：秒 分 时 日 月 星期 年（可选）

字段名 | 允许的值 | 允许的特殊字符
-|-|-
秒 | 0-59 | , - * /
分 | 0-59 | , - * /
时 | 0-23 | , - * /
日 | 1-31 | , - * ? / L W C
月 | 1-12 或 JAN-DEC | , - * /
星期 | 1-7 或 SUN-SAT | , - * ? / L C #
年（可选） | 空 或 1970-2099 | , - * /

**特殊符号说明：**

1、*：通配符，表示该字段可以接收任意值。

2、？ ：表示不确定的值，或不关心它为何值，仅在日期和星期中使用，当其中一个设置了条件时，另外一个用"?" 来表示"任何值"。

3、,：表示多个值，附加一个生效的值。

4、-：表示一个指定的范围

5、/：指定一个值的增量值。例n/m表示从n开始，每次增加m

6、L：用在日期表示当月的最后一天，用在星期"L"单独使用时就等于"7"或"SAT"，如果和数字联合使用表示该月最后一个星期X。例如，"0L"表示该月最后一个星期日。

7、W：指定离给定日期最近的工作日（周一到周五），可以用"LW"表示该月最后一个工作日。例如，"10W"表示这个月离10号最近的工作日

8、C：表示和calendar联系后计算过的值。例如：用在日期中，"5C"表示该月第5天或之后包括calendar的第一天；用在星期中，"5C"表示这周四或之后包括calendar的第 一天。

9、#：表示该月第几个星期X。例6#3表示该月第三个周五。

**cron表达式例子：**

0 \* * * * ? 每分钟触发

0 0 \* * * ? 每小时整触发

0 0 4 * * ? 每天凌晨4点触发

0 15 10 * * ? 每天早上10：15触发

\*/5 \* \* \* \* ? 每隔5秒触发

0 \*/5 \* * * ? 每隔5分钟触发

0 0 4 1 * ? 每月1号凌晨4点触发

0 0 4 L * ? 每月最后一天凌晨3点触发

0 0 3 ? * L 每周星期六凌晨3点触发

0 11,22,33 \* * * ? 每小时11分、22分、33分触发

### 1.3 Main方法

后面不同形式的定时器都用下面的main方法来启动Spring boot上下文。

```java
package com.example.schedulingtasks;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class SchedulingTasksApplication {

    public static void main(String[] args) {
        SpringApplication.run(SchedulingTasksApplication.class);
    }
}
```

### 1.4 简单的例子

```java
package com.example.schedulingtasks;

import java.text.SimpleDateFormat;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ScheduledTasks {

    private static final Logger log = LoggerFactory.getLogger(ScheduledTasks.class);

    private static final SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");

    @Scheduled(cron = "0/10 * * * * ?") //每10秒执行一次
    public void scheduledTaskByCorn() {
        log.info("定时任务开始 ByCorn：{}", dateFormat.format(new Date()));
        scheduledTask();
        log.info("定时任务结束 ByCorn：{}", dateFormat.format(new Date()));
    }

    @Scheduled(fixedRate = 20000) //每20秒执行一次
    public void scheduledTaskByFixedRate() {
        log.info("定时任务开始 ByFixedRate：{}", dateFormat.format(new Date()));
        scheduledTask();
        log.info("定时任务结束 ByFixedRate：{}", dateFormat.format(new Date()));
    }

    @Scheduled(fixedDelay = 30000) //每30秒执行一次
    public void scheduledTaskByFixedDelay() {
        log.info("定时任务开始 ByFixedDelay：{}",dateFormat.format(new Date()));
        scheduledTask();
        log.info("定时任务结束 ByFixedDelay：{}", dateFormat.format(new Date()));
    }

    private void scheduledTask() {
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

关于cron、fixedRate、fixedDelay三者的区别：

1. cron
   如果任务耗时小于定时间隔，那么定时任务按照设定执行；但是如果任务耗时大于设定的时间间隔，那么任务执行完之后，会在下一个满足时间间隔设置的时间执行，不会立即执行漏掉的任务。

2. fixedRate
   如果任务耗时小于定时间隔，那么定时任务按照设定执行；如果任务耗时大于设定的时间间隔，则任务循环执行，也就是上一个任务一结束，立马执行新的任务。

3. fixedDelay
   不论任务耗时时间长短，fixedDelay指定的间隔，都是一次任务完成后，开始新一轮的时间间隔，然后再执行任务。

### 1.5 配置定时任务

添加application.yaml文件：

```yaml
demo:
  cron: 0/11 * * * * ?
```

```java
@Component
public class ScheduledTask {

    @Scheduled(cron = "${demo.cron}")
    public void scheduledTaskByConfig() {
        log.info("定时任务开始 ByConfig：{}", dateFormat.format(new Date()));
    }
}
```

### 1.6 动态修改定时任务

基于接口SchedulingConfigurer，动态生成定时器。

```java
package com.example.schedulingtasks;

import java.text.SimpleDateFormat;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.SchedulingConfigurer;
import org.springframework.scheduling.config.ScheduledTaskRegistrar;
import org.springframework.scheduling.support.CronTrigger;
import org.springframework.stereotype.Component;

@Component
public class ScheduledTasksNew implements SchedulingConfigurer {

    private static final Logger log = LoggerFactory.getLogger(ScheduledTasksNew.class);

    private static final SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");

    private int tag = 0;

    @Override
    public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
        taskRegistrar.addTriggerTask(() -> {
            log.info("定时任务：{}", dateFormat.format(new Date()));
        }, (triggerContext) -> {
            CronTrigger cronTrigger;
            if (tag % 2 == 0) {
                log.info("执行了0/10 * * * * ?");
                cronTrigger = new CronTrigger("0/10 * * * * ?");
                tag++;
            } else {
                log.info("执行了0/20 * * * * ?");
                cronTrigger = new CronTrigger("0/20 * * * * ?");
                tag++;
            }

            return cronTrigger.nextExecutionTime(triggerContext);
        });
    }
}

```

### 1.7 并发定时器任务

上面创建的定时任务都是串行的，一次只会有一个定时任务执行。接下来介绍并发执行定时器任务的方式：

很简单，只需要两个注解即可：@EnableAsync和@Async。

```java
package com.example.schedulingtasks;

import java.text.SimpleDateFormat;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@EnableAsync
public class ScheduledTasks {

    private static final Logger log = LoggerFactory.getLogger(ScheduledTasks.class);

    private static final SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");

    @Scheduled(fixedRate = 5000)
    public void reportCurrentTime() {
        log.info("The time is now {}", dateFormat.format(new Date()));
    }

    @Scheduled(cron = "0/10 * * * * ?") //每10秒执行一次
    @Async
    public void scheduledTaskByCorn() {
        log.info("定时任务开始 ByCorn：{}", dateFormat.format(new Date()));
        scheduledTask();
        log.info("定时任务结束 ByCorn：{}", dateFormat.format(new Date()));
    }

    @Scheduled(fixedRate = 20000) //每10秒执行一次
    @Async
    public void scheduledTaskByFixedRate() {
        log.info("定时任务开始 ByFixedRate：{}", dateFormat.format(new Date()));
        scheduledTask();
        log.info("定时任务结束 ByFixedRate：{}", dateFormat.format(new Date()));
    }

    @Scheduled(fixedDelay = 30000) //每10秒执行一次
    @Async
    public void scheduledTaskByFixedDelay() {
        log.info("定时任务开始 ByFixedDelay：{}",dateFormat.format(new Date()));
        scheduledTask();
        log.info("定时任务结束 ByFixedDelay：{}", dateFormat.format(new Date()));
    }

    private void scheduledTask() {
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```
