[TOC]

# Python代码处理时间和日期

Python中和时间、日期相关的模块有：datetime、calendar、time，以及一个第三方库dateutil。

## 1. time模块

[官方文档参考](https://docs.python.org/3/library/time.html#module-time)

下面介绍几个和时间、日期处理有关的几个函数。

### 1.1 time.time()

获取时间戳，也就是从1970年1月1日午夜开始经历的秒数。

### 1.2 时间元组struct_time

时间戳适合做运算，但是不能直观反映时间的不同组成。Python代码中通常会把时间戳转换为时间元组struct_time，它是一个namedtuple。它有如下几个属性：

- tm_year   年份
- tm_mon    月份1~12
- tm_mday   月内的第几天1~31
- tm_hour   24时第几小时
- tm_min    一个小时内的第几分钟0~59
- tm_sec    第几秒，0~61(61是闰秒)
- tm_wday   0~6，0表示周一
- tm_yday   一年中的第几天，1~366
- tm_isdst  是否为夏令时，1是，0不是，-1未知

获取时间元组的函数：time.localtime([secs])。

### 1.3 格式化时间

time.asctime([t])
time.strftime(format[,t])

注意上面的t是struct_time。

## 2. calendar模块

- calenar.weekday(year,month,day)
  返回给定日期的星期码，0~6。

- calendar.timegm(struct_time)
  功能和time.gmtime相反，接受时间元组，返回时间戳。

## 3. datetime模块

time模块和calendar模块都是用来获取基础时间信息，并对展示形式做简单的处理。如果要进行日期的计算，需要使用datetime模块。

在datetime模块中有timedelta类，这个类的对象用于表示一个时间间隔。

不过datetime功能还是有点鸡肋，所以使用dateutil包。

[datetime参考](https://www.cnblogs.com/awakenedy/articles/9182036.html)

## 4. dateutil

如果需要在时间上做运算，那么使用这个模块的增强版relativedelta功能会更强。

安装：pip install python-dateutil

[官方文档](https://dateutil.readthedocs.io/en/stable/index.html)
