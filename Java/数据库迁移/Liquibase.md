[TOC]

# Liquibase

Liquibase是一种开源的数据库迁移工具（Database migration tool），用于跟踪、管理和应用数据库的变化。

有两种方法来管理数据库更改：状态和迁移方法。

- 第一种方法是基于状态的（或声明性的）的 ， 其中定义了数据库的所需状态。可以通过对应工具将目标环境与定义的所需状态进行比对（或对比），用于生成允许目标环境与声明状态匹配的迁移脚本。
- 另一种方法是基于迁移（或命令的），其中描述了用于更改数据库状态的特定迁移。通过对应工具能够显式跟踪和排序各个迁移，并将尚未部署到目标环境的迁移正确迁移到目标数据库。

虽然Liquibase能够进行比对（或对比），但它从根本上说是基于迁移的解决方案。Liquibase的比对能力仅用于协助加入新项目，并检查数据库迁移是否得到正确应用。作为基于迁移的解决方案，Liquibase 可以轻松：

- 跟踪所有建议的数据库更改，包括需要部署的特定顺序、建议/创作更改的人员，并记录更改的目的（作为注释）

- 清楚地回答数据库更改是否已部署到数据库。实际上，Liquibase 能够管理每个数据库的"版本"。

- 确切地将更改部署到数据库，包括将数据库提升为特定的"版本"

- 阻止用户修改已部署到数据库的更改，要么有意重新处理部署的更改，要么前滚。

## 1. Liquibase工作原理

Liquibase的核心是依靠一种简单的机制来跟踪、版本和部署更改：

- Liquibase 使用更改日志（是更改的分类）按特定顺序显式列出数据库更改。更改日志中的每个更改都是一个change set。更改日志可以任意嵌套，以帮助组织和管理数据库迁移。

**注意：** 最佳做法是确保每个change set都尽可能原子性更改，以避免失败的结果使数据库中剩下的未处理的语句处于unknown 状态;不过，可以将大型 SQL 脚本视为单个更改集。

- Liquibase 使用跟踪表（具体称为**DATABASECHANGELOG**），该表位于每个数据库上，并跟踪已部署更改日志中的change set。

**注意：** 如果 Liquibase所在的数据库没有跟踪表，Liquibase 将创建一个跟踪表。
**注意：** 为了协助处理您未从空白数据库开始的项目，Liquibase具有生成一条更改日志以表示数据库模式当前状态的功能。

使用分类和跟踪表，Liquibase 能够：

- 跟踪和以版本控制数据库更改 – 用户确切知道已部署到数据库的更改以及尚未部署的更改。
- 部署更改 — 具体来说，通过将分类(ledger)中的内容与跟踪表中的内容进行比较，Liquibase 只能将以前尚未部署到数据库的更改部署到数据库中。

**注意：** Liquibase 具有上下文、标签和先决条件等高级功能，可精确控制changeSet的部署时间以及位置。

## 2. Liquibase特点

- 不依赖于特定的数据库，支持几乎所有主流的数据库，如MySQL, PostgreSQL, Oracle, Sql Server, DB2等；
- 支持多开发者的协作维护；
- 日志文件支持多种格式，如XML, YAML, JSON, SQL等；
- 支持多种运行方式，如命令行、Spring集成、Maven插件、Gradle插件等。

## 3. 结合Spring Boot使用

### 3.1 引入依赖

这里以Maven为例：

```xml
<dependencies>
    <dependency>
        <groupId>org.liquibase</groupId>
        <artifactId>liquibase-core</artifactId>
    </dependency>
    <dependency>
</dependencies>
```

### 3.2 配置日志文件

1. 在resources目录中创建/db/changelog目录作为日志文件存放目录
2. 在目录中创建日志文件db.changelog-master.yml
3. 在application.yml中配置changelog路径：

```yaml
spring:
  liquibase:
    # 不配置默认会查找'classpath:/db/changelog/db.changelog-master.yaml'文件
    change-log: 'classpath:/db/changelog/db.changelog-master.yml'
```

### 3.3 编写ChangeSet

1. 编写初始ChangeSet

```yaml
databaseChangeLog:
  - changeSet:
      # 唯一id，建议使用Flayway的命名格式'V<version>[_<SEQ>][__description]'
      id: V1.0_0__init
      # 作者
      author: Cheivin
      # 描述
      comment: "初始化脚本内容，加载初始数据"
      # 启用事物
      runInTransaction: true
      # 变更脚本
      changes:
        # 创建表格
        - createTable:
            tableName: user
            columns:
              - column:
                  name: id
                  type: int
                  autoIncrement: true
                  constraints:
                    primaryKey: true
                    nullable: false
                  remarks:
              - column:
                  name: username
                  type: VARCHAR(50)
                  constraints:
                    nullable: false
              - column:
                  name: password
                  type: VARCHAR(50)
                  constraints:
                    nullable: false
        # 加载数据
        - loadData:
            tableName: user
            columns:
              - column:
                  header: username
                  name: username
              - column:
                  header: password
                  name: password
            encoding: UTF-8
            file: db/data/init-data.csv
        # 标记，用于回滚时指定版本
        - tagDatabase:
            tag: V1.0_0__init
```

2. 运行项目
3. 添加新的修改

```yaml
# 在databaseChangeLog后追加
  - changeSet:
      id: V1.0_1__mod
      author: Cheivin
      comment: "修改用户表，增加账单表"
      runInTransaction: true
      changes:
        # 通过标准格式添加字段
        - addColumn:
            # 目标表
            tableName: user
            columns:
              - column:
                  name: state
                  type: tinyint
                  # 默认值
                  defaultValueNumeric: 0
                  remarks: '用户状态,0:未激活,1:激活,-1:禁用'
              - column:
                  name: identity
                  type: int
                  # 默认值
                  defaultValueNumeric: 999
                  remarks: '用户身份，999:管理员'
        # 通过sql语句操作数据库
        - sql:
            sql: insert into user (username,password,state,identity) values ('admin','admin',1,999)
        # 通过sql文件操作数据库
        - sqlFile:
            encoding: utf8
            path: db/changelog/V1.0_1__mod_bill.sql
        - tagDatabase:
            tag: V1.0_1__mod
        # 回滚语句
        - rollback:
            - delete:
                tableName: user
                where: username='admin'
            - dropTable:
                tableName: user_bill
```

## 4. 纯Maven中使用

### 4.1 引入依赖

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.liquibase</groupId>
            <artifactId>liquibase-maven-plugin</artifactId>
            <version>3.6.3</version>
            <configuration>
              <!-- 配置文件，必须放在resource目录下 -->
              <propertyFile>src/main/resources/liquibase/liquibase.properties</propertyFile>
            </configuration>
            <executions>
                <!-- 默认mvn启动时执行更新操作 -->
                <execution>
                    <phase>process-resources</phase>
                    <goals>
                        <goal>update</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### 4.2 配置liquibase.properties

```txt
# 日志文件路径，必须放在resource目录下
changeLogFile=src/main/resources/liquibase/db.changelog-master.yml
# 数据库地址
url=jdbc:mysql://localhost:3306/liquibase_mvn?useSSL=false&useUnicode=true&characterEncoding=UTF-8
# 账号
username=root
# 密码
password=root
```

后面的内容和SpringBoot的操作一样。

## 5. Liquibase使用规范

- ChangeSet id建议使用Flayway的命名格式V\<version>[_\<SEQ>][__description],如V1.0_0__init。或使用[任务ID]-[日期]-[序号]，如T100-20190705-001
- ChangeSet必须填写author
- Liquibase禁止对业务数据进行sql操作
- 所有表，列要加remarks进行注释
- 已经执行过的ChangeSet严禁修改。
- 不要随便升级项目liquibase版本，特别是大版本升级。不同版本ChangeSet MD5SUM的算法不一样。

## 参考

1. [Liquibase使用](https://blog.csdn.net/zhao0416/article/details/94733610)
2. [Liquibase配置文档](http://www.liquibase.org/documentation/changes/index.html)
