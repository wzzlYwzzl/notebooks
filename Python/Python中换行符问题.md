# Python换行问题

在Python 3中，open函数有一个newline参数用于控制换行符。

- 当读取时：
默认开启Universal new line mode，也就是会将\n, \r, 或者 \r\n都转换为\n。
如果你希望换行符保持文件自身的换行符，可以把newline=''。

- 写入时：
如果不指定newline，那么换行符会根据各个系统默认的换行符，如果指定newline，那么就会用指定的换行符。
