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

### 2.2 删除binlog日志

## binlog日志的格式

## Mysql日志优化
