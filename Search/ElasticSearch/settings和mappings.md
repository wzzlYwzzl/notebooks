[TOC]

# ES索引的settings和mappings

settings配置的是索引层面的内容，比如索引有几个副本、多少shard片，以及自定义analyzer。

mappings定义的Document的信息，类似于数据库的schema，用于定义Document字段的类型、使用什么analyzer、是否索引、是否存储等信息。甚至可以不用设置mappings，ES可以动态根据添加的Document来修改mappings。但是如果要设置是否分词、是否存储、使用哪个analyzer，那么就需要设置手动设置mappings。

## settings使用举例

这里以创建知识图谱的三元组的索引“triple”为例来介绍如何使用settings。

```json
{
  "settings": {
    "number_of_shards":3, //设置shards大小
    "number_of_replicas":2, //副本数量
    "analysis": {
      "filter": {
        "jieba_stop": {
          "type": "stop",
          "stopwords_path": "stopwords/stopwords.txt"
        },
        "jieba_synonym": {
          "type": "synonym",
          "synonyms_path": "synonyms/synonyms.txt"
        }
      },
      "analyzer": {
        "my_ana": {
          "tokenizer": "jieba_index",
          "filter": [
            "lowercase",
            "jieba_stop",
            "jieba_synonym"
          ]
        }
      }
    }
  }
}
```

注意：

- 不存在索引时，可以指定副本和分片；
- 如果存在索引，则只能修改副本。

## mappings

mappings和settings在Json对象中是处在同一级别的。

前面也说了，mappings是定义文档层面的信息。mappings包括两部分：

- Meta-fields
  用于配置文档的metadata如何处理。比如 _index, _type, _id, and _source fields。
  - _index：文档属于哪个index
  - _type：自定义的名字，每一个index都有一个mapping type，里面的内容就是fields信息。z

- Fields or properties
  配置文档字段信息。一个properties至少有两部分，名字，type，还有一些其他的[mappings的参数](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-params.html)。

例如：

```json
{
  "mappings": {
    "properties": {
      "age":    {
        "type": "integer",
        "analyzer": "my_analyzer",
        "term_vector": "yes"
      },
      "email":  { "type": "keyword"  },
      "name":   { "type": "text"  }
    }
  }
}
```

### Field datatype

type类型包括：

[官网说明](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)

- string类型的，比如text和keyword
- 数字类型的，比如long, integer, short, byte, double, float, half_float, scaled_float
- Date类型：date
- Boolean类型：boolean
- Binary类型：binary
- Range类型：integer_range, float_range, long_range, double_range, date_range
- Complex类型：Object或者Object的数组
- 地理位置型：geo-point、geo-shape
- 专门的数据类型：
- Arrays
- Multi-Fields
