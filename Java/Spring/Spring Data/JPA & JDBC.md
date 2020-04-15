[TOC]

# JDBC & JPA

## 1. JPA

Java Persistence API，它是Sun公司设计的一套持久化API，是一套**ORM规范、标准、接口**。

### 1.1 ORM

JPA是一套ORM规范，那么什么是ORM呢？

ORM，Object Relational Mapping，对象关系映射。将对象和数据库表关联起来，通过直接操作数据对象来实现对数据库的操作，而无需编写SQL语句，由框架来自动生成SQL语句。

### 1.2 JPA的实现

JPA只是一套理论接口，没有具体的实现。市面上的主流JPA实现有：Hibernate （JBoos）、EclipseTop（Eclipse社区）、OpenJPA （Apache基金会）。 其中，Hibernate是性能最好的一个实现。

## 2. JDBC

Java Database Connectivity，Java操作**数据库的原生API**。JDBC提供的是一种统一的访问数据库的方式，不论底层的数据库是何种，Mysql、Sqlserver等等，都可以利用JDBC这套接口来访问。接口的实现由不同的数据库提供商来完成。

## 3. JDBC & JPA

这两者不是一个层面的设计，JDBC侧重于底层数据库的访问；JPA则是ORM的规范，是为了用模型的角度的看待数据，是对底层存储的有一层抽象，其实底层和数据库打交道还是要使用JDBC接口。

## 4. Spring Data JPA & hibernate & mybatis

spring data jpa是对jpa规范的再次抽象，底层还是用的实现jpa的hibernate技术。

hibernate是一个标准的orm框架，实现jpa接口。

mybatis也是一个持久化框架，但不完全是一个orm框架，不是依照的jpa规范。
