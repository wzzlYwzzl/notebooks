[TOC]

# Spring Boot配置多个DataSource

Spring Boot的一大亮点就是自动配置。当我们使用Spring Boot访问数据库时，只要我们引入了某些依赖，Spring Boot就会为我们自动创建一个DataSource。如果我们在application.yml中指定了DataSource的配置，那么Spring Boot就会为我们创建一个相应的DataSource。

但是，有时我们需要在一个应用中访问多个数据库，那么就需要显式干涉DataSource的创建过程。

下面举例说明这个过程需要哪些操作。

## 1. 配置多个DataSource

配置多个DataSource的过程可以总结为：

1. pom.xml文件中添加依赖：可能需要的不同数据库驱动；
2. application.yaml文件中添加datasource配置；
3. 创建两个DataSource的Bean；
4. 紧接着，创建两个JdbcTemplate的Bean；
5. 在具体Service代码中注入相应的JdbcTemplate即可。

### 1.1 appliation.yaml中添加如下两个DataSource的配置

假设我们需要访问两个不同的数据库如下配置：

```yaml
spring:
  datasource:
    test:
      # 使用druid数据源
      type: com.alibaba.druid.pool.DruidDataSource
      jdbc-url: jdbc:mysql://localhost:3306/test?serverTimezone=CTT&useUnicode=true&characterEncoding=utf-8&allowMultiQueries=true
      username: root
      password: root
      driver-class-name: com.mysql.jdbc.Driver

    test1:
      # 使用druid数据源
      type: com.alibaba.druid.pool.DruidDataSource
      jdbc-url: jdbc:oracle:thin:@172.16.182.18:1521:orcl
      username: policyprint
      password: sinosoft
      driver-class-name: oracle.jdbc.OracleDriver
```

### 1.2 创建两个DataSource的bean

```java
@Configuration
public class SomeConfiguration {
    @Bean
    @Primary
    @ConfigurationProperties(prefix = "spring.datasource.test")
    public DataSource primaryDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean(name = "secondDatasource") //多个类型相同的bean，需要为其指定name，否则会抛异常。
    @ConfigurationProperties(prefix = "spring.datasource.test1")
    public DataSource secondDataSource() {
        return DataSourceBuilder.create().build();
    }
}
```

### 1.3 创建两个JdbcTemplate的Bean

```java
@Bean
@Primary //多个类型相同的，建议用这个注解，优先注入这个
public JdbcTemplate primaryJdbcTemplate(DataSource dataSource) {
    return new JdbcTemplate(dataSource);
}

@Bean(name = "secondJdbcTemplate")
public JdbcTemplate secondJdbcTemplate(@Qualifier("secondDatasource") DataSource dataSource) {
    return new JdbcTemplate(dataSource);
}
```

### 1.4 在业务代码中注入JdbcTemplate

```java
@Component
public class SomeService {
    @Autowired //因为定义的JdbcTemplate有一个使用了@Primary，所以可以不用@Qualifier
    JdbcTemplate jdbcTemplate;
}
```

```java
@Component
public class AnotherService {
    @Autowired
    @Qualifier("secondJdbcTemplate") //因为同类型的有多个，需要指定bean名称
    JdbcTemplate secondJdbcTemplate;
}
```

## 参考

1. [Spring Boot配置多个DataSource](https://www.liaoxuefeng.com/article/1127277451217344)
