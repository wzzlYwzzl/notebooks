[TOC]

# Pymysql

python 3.0之后的mysql数据库驱动。

## 通过列名访问查询结果

通过指定游标类型，默认是数组的访问方式。

```python
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
```

## 参考

1. [官方简单教程](https://docs.microsoft.com/zh-cn/sql/connect/python/pymssql/step-3-proof-of-concept-connecting-to-sql-using-pymssql?view=sql-server-ver15)
2. [](http://www.pymssql.org/en/stable/pymssql_examples.html)
