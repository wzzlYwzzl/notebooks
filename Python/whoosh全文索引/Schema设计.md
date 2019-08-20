[TOC]

# Whoosh的Schema设计

Schema类似于传统数据库的Schema一样，用于说明index中document的结构的。

一个document可以有多个field，有些field是can be stored with the document，对于这些field，是可以在搜索结果中展示的；有些字段是既可以indexed，又可以stored。

schema定义的是可能的fields，这意味着一个document可以只包含这些fields的子集。

## 1. 内置field type

### 1.1 whoosh.fields.TEXT

这表示这个field被indexed，是否stored是一个可选项。默认使用的analyzer是StandardAnalyzer，也可以通过在TEXT的构造函数中指定不同的analyzer，比如TEXT(analyzer=analysis.StemmingAnalyzer())。

TEXT字段会存储每个indexed term的位置信息，允许通过phrases搜索。如果不需要search for phrases，可以在构造函数中指定(phrase=False)。

默认，TEXT字段是not stored，同常，是没有必要把这个字段的原始信息存储到index中的。

### 1.2 whoosh.fields.KEYWORD

这个字段类型是为空格分隔或者逗号分隔的关键词的。这种类型是indexed and searchable，可选的stored。为了节省空间，不支持phrase searching。

为了存储value到index中，可以在构造函数中使用(stored=True)，如果需要在构建索引时，转换为小写，可以在构造函数中使用(lowercase=True)。

默认，keywords是用逗号分隔的，如果是逗号分隔，可以通过(commas=True)来指定。如果用户需要用这个field来搜索，可以使用(scorable=True)。

### 1.3 whoosh.fields.ID

ID类型的field表示这个字段作为一个整体被indexed。

ID类型可以用于url、path、date等等。

ID类型默认是not stored，可以通过在构造函数中传入(stored=True)来指定stored。

### 1.4 whoosh.fields.STORED

这种类型的field不会indexed，也是not searchable。它可以应用于需要展示给用户，但是不允许用户搜索的字段。

### 1.5 whoosh.fields.NUMERIC

int、long、floating等数据。

### 1.6 whoosh.fields.DATETIME

存储日期对象以紧凑、可排序的方式。

### 1.7 whoosh.fields.BOOLEAN

index bool类型的值，允许用户通过yes、no、true、false、1、0、t、f来搜索这个field。

## 2. 创建Schema的方式

```python
from whoosh.fields import *
from whoosh.anaysis import StemmingAnalyzer

schema = Schema(from_addr=ID(stored=True),
                to_addr=ID(stored=True),
                subject=TEXT(stored=True),
                body=TEXT(anayzer=StemmingAnalyzer()),
                tags=KEYWORD)
```

## 3. 构建索引后修改schema

构建完索引后，仍旧可以通过add_field和remove_field来添加或者删除field。

## 4. 更多内容

[whoosh schema](https://whoosh.readthedocs.io/en/latest/schema.html)
