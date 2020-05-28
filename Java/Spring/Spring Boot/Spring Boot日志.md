[TOC]

# Spring Boot日志

与Java有关的日志框架有：JCL、SLF4j、Jboss-logging、jUL、log4j、logback等，这些可以分为两类：日志抽象层和日志实现层。

日志抽象层：JCL,SLF4J,jboss-logging
日志实现层：jul、log4j、log4j2、logback

SpringBoot选择的组合是：SLF4j + Logback。

## 1. 屏蔽其他日志框架

有时，我们使用其他模块会引入与SpringBoot不一样的日志框架，可以将其移除。

```xml
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-core</artifactId>
  <exclusions>
    <exclusion>
      <groupId>commons-logging</groupId>
      <artifactId>commons-logging</artifactId>
    <exclusion>
  </exclusions>
```

## 2. Spring Boot日志功能使用

操作很简单，只需一句话，就可以使用相应的logger输出日志信息。

```java
Logger logger = LoggerFactory.getLogger(xxx.class)

//后面可以通过logger输出日志
logger.info(...)
logger.error(...)
```

## 3. 指定日志的级别

框架设计上，日志有六个级别：TRACE、DEBUG、INFO、WARN、ERROR、FATAL。

Spring Boot可以在两个层次上配置日志的级别，一个是root级别，即项目的所有日志；还有就是package级别，指定某个包内的日志级别。

```txt
# root级别配置
logging.level.root = warn

# package级配置，后面的xx表示包的路径
logging.level.xx.xxx.xxx = error
```

## 4. 指定日志的路径和文件名称

**logging.path**用于指定日志的文件的路径。
**logging.file**用于指定日志文件

```txt
logging.path = output/logs
logging.file = my.log
```

## 5. 指定日志的格式

%d：时间格式
%thread ：线程
%-5level ：日志级别从左5字符宽度、
%logger{50}：日志输出者的名字，50个字符
%msg：信息
%n：换行

```txt
# 修改在控制台输出的日志格式
logging.pattern.console=%d{yyyy-MM-dd} [%thread] %-5level %logger{50} -%msg%n
# 修改输出到文件的日志格式
logging.pattern.file=%d{yyyy/MM/dd} === [%thread] == %-5level == %logger{50} == %msg%n
```
