[TOC]

# MySQL字段类型与Java类型映射
  
|  类型名称  |  显示长度  |  数据库类型  |  JAVA类型  |  JDBC类型索引(int)  |
|  -  |  -  |  -  |  -  |  -  |  
VARCHAR  |  L+N  |  VARCHAR  |  java.lang.String  |  12
CHAR  |  N  |  CHAR  |  java.lang.String  |  1
BLOB  |  L+N  |  BLOB  |  java.lang.byte[]  |  -4
TEXT  |  65535  |  VARCHAR  |  java.lang.String  |  -1
INTEGER  |  4  |  INTEGER UNSIGNED  |  java.lang.Long  |  4
TINYINT  |  3  |  TINYINT UNSIGNED  |  java.lang.Integer  |  -6
SMALLINT  |  5  |  SMALLINT UNSIGNED  |  java.lang.Integer  |  5
MEDIUMINT  |  8  |  MEDIUMINT UNSIGNED  |  java.lang.Integer  |  4
BIT  |  1  |  BIT  |  java.lang.Boolean  |  -7
BIGINT  |  20  |  BIGINT UNSIGNED  |  java.math.BigInteger  |  -5
FLOAT  |  4+8  |  FLOAT  |  java.lang.Float  |  7
DOUBLE  |  22  |  DOUBLE  |  java.lang.Double    8
DECIMAL  |  11  |  DECIMAL  |  java.math.BigDecimal  |  3
BOOLEAN  |  1  |  同TINYINT
ID  |  11  |  PK (INTEGER UNSIGNED)  |  java.lang.Long  |  4
DATE  |  10  |  DATE  |  java.sql.Date  |  91
TIME  |  8  |  TIME  |  java.sql.Time  |  92
DATETIME  |  19  |  DATETIME  |  java.sql.Timestamp  |  93
TIMESTAMP  |  19  |  TIMESTAMP  |  java.sql.Timestamp  |  93
YEAR  |  4  |  YEAR  |  java.sql.Date  |  91
