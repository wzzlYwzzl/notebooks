[TOC]

# binlog增量订阅

通过解析binlog来获取数据库的修改操作有两种方式：

- 通过外部程序监听磁盘上的binlog日志文件；
- 借助Mysql的master-slave结构，使程序伪装成单独的slave，通过网络获取Mysql的binlog日志。

不论哪种方式，一般都要求binlog的格式是Row。

## 解决方案

### 阿里巴巴的canal

[github地址](https://github.com/alibaba/canal)

工作原理：

**mysql主备复制实现，从上层来看，复制分成三步：**

- master将改变记录到二进制日志(binary log)中（这些记录叫做二进制日志事件，binary log events，可以通过show binlog events进行查看）；
- slave将master的binary log events拷贝到它的中继日志(relay log)；
- slave重做中继日志中的事件，将改变反映它自己的数据。

**canal的工作原理相对比较简单：**

- canal模拟mysql slave的交互协议，伪装自己为mysql slave，向mysql master发送dump协议；
- mysql master收到dump请求，开始推送binary log给slave(也就是canal)；
- canal解析binary log对象(原始为byte流)

### Open Replicator

Open Replicator是一个用Java编写的MySQL binlog分析程序。Open Replicator 首先连接到MySQL（就像一个普通的MySQL Slave一样），然后接收和分析binlog，最终将分析得出的binlog events以回调的方式通知应用。Open Replicator可以被应用到MySQL数据变化的实时推送，多Master到单Slave的数据同步等多种应用场景。开源地址：http://code.google.com/p/open-replicator

[github源码](https://github.com/whitesock/open-replicator)

### mysql-binlog-connector-java

[github源码](https://github.com/shyiko/mysql-binlog-connector-java)

### maxwell

[Github源码](https://github.com/zendesk/maxwell)
[官网](http://maxwells-daemon.io/)

maxwell是一个由Java编写的守护进程，可以实时读取mysql binlog并将行更新以JSON格式写入Kafka，Kinesis，RabbitMQ，Google Cloud Pub / Sub或Redis（Pub / Sub或LPUSH）。（以上内容摘自maxwell官网）。可以想象，有了mysql增量数据流，使用场景就很多了，比如：实时同步数据到缓存，同步数据到ElasticSearch，数据迁移等等。与canal(ali)相比，更加轻量

maxwell还提供以下功能：

- 使用SELECT * FROM table 的方式做全量数据初始化
- 支持主库发生failover后，自动恢复binlog位置
- 对数据进行分区，解决数据倾斜的问题
- 伪装成mysql从库，接收binlog

### python-mysql-replication

[github源码](https://github.com/noplay/python-mysql-replication)

python-mysql-replication是基于MySQL复制原理实现的，把自己伪装成一个slave不断的从MySQL数据库获取binlog并解析。

[中文cnblog](https://www.cnblogs.com/zhangjianhua/p/8080538.html)

## 参考

1. [Mysql binlog增量数据解析服务](http://itindex.net/detail/58805-mysql-binlog-%E6%95%B0%E6%8D%AE)
