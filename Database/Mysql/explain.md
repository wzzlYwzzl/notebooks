[TOC]

# Mysql Explain

Mysql中通过explain可以查看SQL语句的执行计划。具体查看哪些信息，后面会逐步介绍。

## 1. explain使用

使用方法很简单，就是在SQL语句前面添加explain关键词就可以了。

```sql
select * from emp where name='jack'

explain select * from emp where name='jack'
```

## 2. explain返回哪些信息

explain命令会返回10列内容，分别为：

- id
- select_type
- table
- type
- possible_keys
- key
- key_len
- ref
- rows
- Extra

接下来分别介绍每个字段的含义。

### 2.1 id

select的查询序列号。具体的顺序逻辑是：

1. id相同时，执行顺序从上到下；
2. 如果是子查询，id的序号会递增，id值越大优先级越高，越先被执行；
3. id相同，则认为是一组，从上往下顺序执行；

### 2.2 select_type

select语句的类型。

- SIMPLE：简单select，不包含UNION或子查询等；
- PRIMARY：查询中若包含任何复杂的子部分，最外层的select被标记为PRIMARY；
- UNION：UNION中的第二个或后面的SELECT语句；
- DEPENDENT UNION：UNION中的第二个或后面的SELECT语句，取决于外面的查询；
- UNION RESULT：UNION的结果，union语句中第二个select开始后面所有的select；
- SUBQUERY：子查询中的第一个SELECT，结果不依赖于外部查询；
- DEPENDENT SUBQUERY：子查询的第一个SELECT，依赖于外部查询；
- DERIVED：派生表的SELECT，FROM子句的子查询；
- UNCACHABLE SUBQUERY：一个子查询的结果不能被缓存，必须重新评估链接的第一行；

### 2.3 table

这一步锁访问的数据库表名。有时不是真实的表别名，可能是简称，也可能是第几步执行的结果的简称。

### 2.4 type

对表的访问方式，也就是在表中找到相应行的方式。

有以下几种类型：ALL、index、range、ref、eq_ref、const、system、NULL。

这几种性能从左到右，逐渐变好。

1. ALL
   遍历全表。

2. index
   索引树全遍历。

3. range
   只检索给定范围的行，使用一个索引来选择行。

4. ref
   表示哪些列或常量被用于查找索引列上的值。

5. eq_ref
   类似ref，区别在于使用的索引是唯一索引。

6. const,system
   性能是常量，比如对主键执行where查询。

7. NULL
   执行时不需要访问表或索引。

### 2.5 possible_keys

列出的是查询的字段上有哪些索引可以使用，但是并不一定会被使用。

### 2.6 Key

列出的是Mysql实际决定使用的键（索引），这里的索引必然包含在possible_keys。

如果想要强制Mysql使用或者忽视possible_keys列中的索引，可以在查询中使用FORCE INDEX、USE INDEX或者IGNORE INDEX。

### 2.7 key_len

表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度。

key_len显示的值是索引字段的最大可能长度，并非实际使用的长度，key_len是根据表定义计算而得，而不是通过表内检索得到的。

### 2.8 ref

列与索引的比较，表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值

### 2.9 rows

估算出结果集的行数，表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数。

### 2.10 Extra

- Using where:不用读取表中所有信息，仅通过索引就可以获取所需数据，这发生在对表的全部的请求列都是同一个索引的部分的时候，表示mysql服务器将在存储引擎检索行后再进行过滤

- Using temporary：表示MySQL需要使用临时表来存储结果集，常见于排序和分组查询，常见 group by ; order by

- Using filesort：当Query中包含 order by 操作，而且无法利用索引完成的排序操作称为“文件排序”

- Using join buffer：改值强调了在获取连接条件时没有使用索引，并且需要连接缓冲区来存储中间结果。如果出现了这个值，那应该注意，根据查询的具体情况可能需要添加索引来改进能。

- Impossible where：这个值强调了where语句会导致没有符合条件的行（通过收集统计信息不可能存在结果）。

- Select tables optimized away：这个值意味着仅通过使用索引，优化器可能仅从聚合函数结果中返回一行

- No tables used：Query语句中使用from dual 或不含任何from子句