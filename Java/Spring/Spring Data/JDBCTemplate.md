[TOC]

# JDBCTemplate

它是由Spring JDBC引入，JDBCTemplate是对JDBC接口的进一步封装。使用jdbc时,每次都需要自己获取PreparedStatement，输入sql语句参数，关闭连接等操作。造成操作冗余。影响我们打代码的效率。有了JDBCTemplate以后就可以只写SQL语句就可以了。

JdbcTemplate是Spring的一部分,是对数据库的操作在jdbc的封装,处理了资源的建立和释放(不需要我们管理连接了),我们只需要提供SQL语句(不需要我们设置参数了)和提取结果(查询时候可以直接返回对应的实体类),使JDBC更加易于使用。

JdbcTemplate使用spring的注入功能，把DataSource注册到JdbcTemplate之中。

JdbcTemplate主要提供以下四类方法：

- execute方法：可以用于执行任何SQL语句，一般用于执行DDL语句；
- update方法及batchUpdate方法：update方法用于执行**新增、修改、删除**等语句；batchUpdate方法用于执行批处理相关语句；
- query方法及queryForXXX方法：用于执行查询相关语句；
- call方法：用于执行存储过程、函数相关语句。

## 1. JdbcTemplate数据查询



## 2. JdbcTemplate数据插入

jdbcTemplate插入数据的方式有：

- 直接sql语句；
- 参数替换；
- 通过statement；
- 插入并返回主键id；
- 批量插入；

相关的方法有如下几个：

- update(sql)
- update(sql, param1, param2...)
- update(sql, new PreparedStatementCreator(){})
- update(new PreparedStatementSetter(){})
- update(new PreparedStatementCreator(){}, new GeneratedKeyHolder())

## 3. JdbcTemplate数据更新和删除

## 参考

1. [JdbcTemplate之数据查询上篇](http://spring.hhui.top/spring-blog/2019/04/12/190412-SpringBoot%E9%AB%98%E7%BA%A7%E7%AF%87JdbcTemplate%E4%B9%8B%E6%95%B0%E6%8D%AE%E6%9F%A5%E8%AF%A2%E4%B8%8A%E7%AF%87/)
2. [JdbcTemplate之数据查询下篇](http://spring.hhui.top/spring-blog/2019/04/17/190417-SpringBoot%E9%AB%98%E7%BA%A7%E7%AF%87JdbcTemplate%E4%B9%8B%E6%95%B0%E6%8D%AE%E6%9F%A5%E8%AF%A2%E4%B8%8B%E7%AF%87/)
3. [JdbcTemplate之数据插入使用姿势详解](http://spring.hhui.top/spring-blog/2019/04/07/190407-SpringBoot%E9%AB%98%E7%BA%A7%E7%AF%87JdbcTemplate%E4%B9%8B%E6%95%B0%E6%8D%AE%E6%8F%92%E5%85%A5%E4%BD%BF%E7%94%A8%E5%A7%BF%E5%8A%BF%E8%AF%A6%E8%A7%A3/)
4. [JdbcTemplate之数据更新与删除](http://spring.hhui.top/spring-blog/2019/04/18/190418-SpringBoot%E9%AB%98%E7%BA%A7%E7%AF%87JdbcTemplate%E4%B9%8B%E6%95%B0%E6%8D%AE%E6%9B%B4%E6%96%B0%E4%B8%8E%E5%88%A0%E9%99%A4/)
