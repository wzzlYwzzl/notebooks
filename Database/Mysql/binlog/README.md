[TOC]

# Mysql binlog

Mysql数据库的一种类型的日志，用于记录数据库上发生的修改、变化。注意，这个变化可能不一定真的发生，比如执行没有匹配任何数据的Delete语句，这个语句也会被记录到binlog。

binlog的核心作用就是数据库的备份。通过binlog记录的主数据库的操作，可以完全还原主数据库的内容。可以用在数据的恢复、主从模式的备份。

mysql按照功能分为服务层模块和存储引擎层模块，服务层负责客户端连接、SQL 语句处理优化等操作，存储引擎层负责数据的存储和查询；binlog属于服务层模块的日志，即引擎无关性，所有数据引擎的数据更改都会记录binlog日志。当数据库发生崩溃时，如果使用InnoDB引擎，binlog日志还可以检验InnoDB的redo日志的commit情况。

## 1. 与binlog有关的配置

在mysql的my.cnf配置文件中有如下与binlog相关的配置或参数：

- log_bin: 设置此参数就表示启动binlog功能，并指定路径名称。
- log_bin_index: 指定二进制索引文件的路径和名称。
- binlog_do_db: 此参数表示只记录指定数据库的二进制日志。
- binlog_ignore_db: 不记录指定的数据库的二进制日志。
- max_binlog_cache_size: binlog使用的内存的最大尺寸。
- binlog_cache_size: 此参数表示binlog使用的内存大小，可以通过状态变量binlog_cache_use和binlog_cache_disk_use帮助测试。
- binlog_cache_use: 使用二进制日志缓存的事务数量。
- binlog_cache_disk_use:使用二进制日志缓存但超过binlog_cache_size值并使用临时文件来保存事务中的语句的事务数量。
- max_binlog_size: Binlog最大值，最大和默认值是1GB，该设置并不能严格控制Binlog的大小，尤其是Binlog比较靠近最大值而又遇到一个比较大事务时，为了保证事务的完整性，不可能做切换日志的动作，只能将该事务的所有SQL都记录进当前日志，直到事务结束。
- sync_binlog: 这个参数直接影响mysql的性能和完整性。sync_binlog=0当事务提交后，Mysql仅仅是将binlog_cache中的数据写入Binlog文件，但不执行fsync之类的磁盘同步指令通知文件系统将缓存刷新到磁盘，而让Filesystem自行决定什么时候来做同步，这个是性能最好的。sync_binlog=n，在进行n次事务提交以后，Mysql将执行一次fsync之类的磁盘同步指令，同志文件系统将Binlog文件缓存刷新到磁盘。Mysql中默认的设置是sync_binlog=0，即不作任何强制性的磁盘刷新指令，这时性能是最好的，但风险也是最大的。一旦系统绷Crash，在文件系统缓存中的所有Binlog信息都会丢失。

## 2. 与binlog有关的操作

### 2.1 查看binlog日志

```shell
# 查看binlog日志列表
mysql>show master logs;
# 查看binlog日志文件大小
mysql>show binary logs;
# 查看master binlog日志文件的状态信息
mysql>show master status;

# 产生一个新的binlog日志文件
mysql>flush logs;

# 查看binlog日志的第一个文件的内容
mysql>show binlog events;

# 查看指定binlog文件的内容
mysql>show binlog events in 'binlog.000002'
```

### 2.2 删除binlog日志

有两种方式：手动删除和自动删除。

**设置自动删除binlog：**

```shell
mysql>show variables like 'expire_logs_days';
# 这个参数表示binlog过期的天数，设置为0表示不自动删除
mysql>set global expire_logs_days=3;
# 表示日志保留三天
```

**手动删除binlog：**

```shell
# 删除master的binlog日志
mysql>reset master;
# 删除slave的中继日志
mysql>reset slave;
# 删除指定日期以前的日志索引中的binlog日志文件
mysql>purge master logs before '2012-03-30 17:20:00'
# 删除指定日志文件的binlog
mysql>purge master logs to 'binlog.000002'

# 如果用户有super权限，可以启用或禁止当前会话的binlog记录
mysql>set sql_log_bin=1或0
```

## binlog日志的格式

Mysql的binlog有三种日志格式：Statement、Mixed、Row。可以通过执行如下脚本查看：
>> show global variables like '%binlog_format%'

### Statement

每一条会修改数据的SQL都会记录在binlog中。

**优点**：由于是记录SQL，所以不需要记录每一行的变化，减少了binlog日志量，可以减少IO，提高性能。（注意：减少日志量，同常是指的那些带条件的update操作、整表删除、alter表等操作，这些操作一次性修改大量的数据。如果只是修改一条记录，那么Row反而更能减少日志量。）

**缺点**：由于记录的只是执行的语句，所以为了保证这些语句在slave上正确运行，还必须记录每条SQL执行时候的一些相关信息，以保证所有语句能够在slave上得到和master一样的结果。另外mysql 的复制,像一些特定函数功能，slave可与master上要保持一致会有很多相关问题(如sleep()函数， last_insert_id()，以及user-defined functions(udf)会出现问题)。

### Row

不记录SQL语句，紧保留那条语句被修改。

**优点**：binlog不需要记录执行SQL的上下文信息，只需要记录哪一条被修改成了什么样。Row日志是最细粒度，所以能够清楚记录每一行数据的修改细节，不会出现无法复制的问题。

**缺点**：可能产生大量的日志。

### Mixed

是上面两种方式的混合。一般的修改语句使用statement格式来保存binlog，如果一些函数，statement无法完成主从复制的操作，则采用row格式来保存binlog。Mysql会根据执行的SQL来区别对待日志形式。

新版本的Mysql中，Row格式的binlog日志也是被优化过的，并不是所有的修改都以Row格式记录日志，比如表结构变更的操作会以statement模式记录，同常的update、delete操作，则是用Row方式记录每一行的变化。

## Mysql日志优化

Mysql主要有以下类型的日志：

- 错误日志：记录mysql运行过程中的错误信息；
- 一般查询日志：记录mysql中正在运行的语句，包括查询、修改、更新等；
- 慢查询日志：记录查询比较耗时的SQL语句；
- binlog日志

记录日志会占用昂贵的IO资源。

默认情况下，系统紧打开错误日志，关闭其他的所有日志。但是，在实际应用场景下，binlog日志也是会被打开的，因为Mysql很多引擎都是通过binlog来进行增量备份的，也是Mysql实现增量复制的基础。

另外，有时候为了优化Mysql的性能，定位执行慢的SQL语句，也会打开慢查询日志。不过，同常系统很少会打开一般查询日志。

在所有日志当中，占比最重，最耗性能的就是binlog日志。

### binlog相关参数及优化

通过下面的命令可以查看与binlog有关的所有配置参数。
>>> show variables like '%binlog%'

MySQL的复制（Replication），实际上就是通过将Master端的Binlog通过利用IO线程通过网络复制到Slave端，然后再通过SQL线程解析Binlog中的日志再应用到数据库中来实现的。所以，Binlog量的大小对IO线程以及Msater和Slave端之间的网络都会产生直接的影响。

MySQL中Binlog的产生量是没办法改变的，只要我们的Query改变了数据库中的数据，那么就必须将该Query所对应的Event记录到Binlog中。那我们是不是就没有办法优化复制了呢？当然不是，在MySQL复制环境中，实际上是是有8个参数可以让我们控制需要复制或者需要忽略而不进行复制的DB或者Table的，分别为：

Binlog_Do_DB：设定哪些数据库（Schema）需要记录Binlog；
Binlog_Ignore_DB：设定哪些数据库（Schema）不要记录Binlog；

Replicate_Do_DB：设定需要复制的数据库（Schema），多个DB用逗号（“,”）分隔；
Replicate_Ignore_DB：设定可以忽略的数据库（Schema）；
Replicate_Do_Table：设定需要复制的Table；
Replicate_Ignore_Table：设定可以忽略的Table；
Replicate_Wild_Do_Table：功能同Replicate_Do_Table，但可以带通配符来进行设置；
Replicate_Wild_Ignore_Table：功能同Replicate_Ignore_Table，可带通配符设置；

通过上面这八个参数，我们就可以非常方便按照实际需求，控制从Master端到Slave端的Binlog量尽可能的少，从而减小Master端到Slave端的网络流量，减少IO线程的IO量，还能减少SQL线程的解析与应用SQL的数量，最终达到改善Slave上的数据延时问题。

实际上，上面这八个参数中的前面两个是设置在Master端的，而后面六个参数则是设置在Slave端的。虽然前面两个参数和后面六个参数在功能上并没有非常直接的关系，但是对于优化MySQL的Replication来说都可以启到相似的功能。当然也有一定的区别，其主要区别如下：

如果在Master端设置前面两个参数，不仅仅会让Master端的Binlog记录所带来的IO量减少，还会让Master端的IO线程就可以减少Binlog的读取量，传递给Slave端的IO线程的Binlog量自然就会较少。这样做的好处是可以减少网络IO，减少Slave端IO线程的IO量，减少Slave端的SQL线程的工作量，从而最大幅度的优化复制性能。当然，在Master端设置也存在一定的弊端，因为MySQL的判断是否需要复制某个Event不是根据产生该Event的Query所更改的数据

所在的DB，而是根据执行Query时刻所在的默认Schema，也就是我们登录时候指定的DB或者运行“USEDATABASE”中所指定的DB。只有当前默认DB和配置中所设定的DB完全吻合的时候IO线程才会将该Event读取给Slave的IO线程。所以如果在系统中出现在默认DB和设定需要复制的DB不一样的情况下改变了需要复制的DB中某个Table的数据的时候，该Event是不会被复制到Slave中去的，这样就会造成Slave端的数据和Master的数据不一致的情况出现。同样，如果在默认Schema下更改了不需要复制的Schema中的数据，则会被复制到Slave端，当Slave端并没有该Schema的时候，则会造成复制出错而停止。

而如果是在Slave端设置后面的六个参数，在性能优化方面可能比在Master端要稍微逊色一点，因为不管是需要还是不需要复制的Event都被会被IO线程读取到Slave端，这样不仅仅增加了网络IO量，也给Slave端的IO线程增加了RelayLog的写入量。但是仍然可以减少Slave的SQL线程在Slave端的日志应用量。虽然性能方面稍有逊色，但是在Slave端设置复制过滤机制，可以保证不会出现因为默认Schema的问题而造成Slave和Master数据不一致或者复制出错的问题。

### 慢查询日志相关参数

通过执行下面的命令可以查看慢查询日志相关配置。
>>> show variables like 'log_slow%';

“log_slow_queries”参数显示了系统是否已经打开SlowQueryLog功能，而“long_query_time”参数则告诉我们当前系统设置的SlowQuery记录执行时间超过多长的Query。在MySQLAB发行的MySQL版本中SlowQueryLog可以设置的最短慢查询时间为1秒，这在有些时候可能没办法完全满足我们的要求，如果希望能够进一步缩短慢查询的时间限制，可以使用Percona提供的microslow-patch（件成为mslPatch）来突破该限制。mslpatch不仅仅能将慢查询时间减小到毫秒级别，同时还能通过一些特定的规则来过滤记录的SQL，如仅记录涉及到某个表的SlowQuery等等附加功能。

打开SlowQueryLog功能对系统性能的整体影响没有Binlog那么大，毕竟SlowQueryLog的数据量比较小，带来的IO损耗也就较小，但是，系统需要计算每一条Query的执行时间，所以消耗总是会有一些的，主要是CPU方面的消耗。如果大家的系统在CPU资源足够丰富的时候，可以不必在乎这一点点损耗，毕竟他可能会给我们带来更大性能优化的收获。但如果我们的CPU资源也比较紧张的时候，也完全可以在大部分时候关闭该功能，而只需要间断性的打开SlowQueryLog功能来定位可能存在的慢查询。
