[TOC]

# ES Analyzer

[关于Analyzer的官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html)

ES在构建索引或者查询索引时，会有一个analysis过程。这个过程将文本转换成tokens或者terms，这些tokens将用于构建倒排索引或者进行搜索。这个analysis过程是通过analyzer这个对象来完成的。

## 什么是Analyzer

[ES自带的Analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)

一个Analyzer其实就是一个容器，它包含三种底层模块：character filters、tokenizers和token filters。

### Character filters

[ES自带的Character filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html)

单个字符级的处理，对原始文本中的字符进行增加、删除、修改等操作。

比如可以用于将印度语的数字转换为拉丁语的阿拉伯数字，移除文本中的html标签等等。

一个Analyzer可以有0个或者多个Character filters，多个filter会依次被应用。

### Tokenizer

[ES自带的Tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html)

这个可以粗略的理解为分词的功能，就是将原始文本分割成一个个的token。

一个Analyzer只能有一个且必须有一个Tokenizer。

### Token filters

[ES自带的Token filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html)

在Token粒度对其进行修改、增删等操作。比如：lowercase这个token filter的作用就是将token转换为小写；stop token filter就是过滤其中的stop words；synonym filter的作用就是会为token引入额外的同义词。

token filter是不能修改token中字符的offset的。

一个Analyzer可以有0或多个token filter。

## 测试Analyzer

```json
// GET http://localhost:9200/index_name/_analyze
{
    "analyzer":"analyzer_name",
    "text":"要测试的文本"
}
```
