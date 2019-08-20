[TOC]

# Python读写配置文件

通过内置的configparser模块来解析配置文件。配置文件可以是*.conf 或者*.ini后缀。

## 配置文件样式

```ini
[db] #这称为一个section
db_port = 3306
db_user = root
db_host = 127.0.0.1
db_pass = xgmtest

[concurrent]
processor = 20
thread = 10
```

## 提供的方法

- read(filename)               直接读取文件内容
- sections()                      得到所有的section，并以列表的形式返回
- options(section)            得到该section的所有option
- items(section)                得到该section的所有键值对
- get(section,option)        得到section中option的值，返回为string类型
- getint(section,option)    得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。

## 样例代码

上面文件的读取代码如下：

```python
# !/usr/bin/env python
# -*- coding:utf-8 -*-  

import ConfigParser
import os

os.chdir("D:\\Python_config")

cf = ConfigParser.ConfigParser()

# cf.read("test.ini")
cf.read("test.conf")

#return all section，返回内容是['db','concurrent']
secs = cf.sections()

# 返回db的所有配置的key，这里返回['db_port','db_user','db_host','db_pass']
opts = cf.options("db")

# 返回key，value键值对。这里返回[('db_port','3306'),
# ('db_user','root'),('db_host','127.0.0.1'),()]
kvs = cf.items("db")

#read by type
db_host = cf.get("db", "db_host") #返回的是str类型
db_port = cf.getint("db", "db_port") #返回int类型
db_user = cf.get("db", "db_user")
db_pass = cf.get("db", "db_pass")

#read int
threads = cf.getint("concurrent", "thread")
processors = cf.getint("concurrent", "processor")
```
