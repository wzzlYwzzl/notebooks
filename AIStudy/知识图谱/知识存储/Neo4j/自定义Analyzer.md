[TOC]

# Neo4j自定义分词Analyzer

Neo4j支持对Node和关系中的string类型的property构建全文索引，相关的说明信息及Cypher语句可以参考[neo4j相关文档](https://neo4j.com/docs/cypher-manual/3.5/schema/index/#schema-index-fulltext-search)，但是默认的用于分词的Analyzer对中文的支持并不好，所以需要定义合适的中文Analyzer。

由于Neo4j的全文索引其实就是直接使用lucene构建的，所以Neo4j的Analyzer其实就是简单对lucene的Analyzer封装一个接口即可以使用。

## 例子

[自定义基于ansj的neo4j插件](https://github.com/wzzlYwzzl/neo4j-ansj-plugin/tree/master)。

这个是我基于Ansj的lucene插件实现的Neo4j的Analyzer插件。

ansj的lucene插件源码可以在[github的ansj项目](https://github.com/NLPchina/ansj_seg/plugin)中找到。

## 编写Neo4j插件的pom.xml配置

关于pom配置可以参考[官网的链接](https://neo4j.com/docs/java-reference/3.5/extending-neo4j/procedures-and-functions/procedures-setup/)。

## 参考

1. [Custom analyzer for fulltext search](https://graphaware.com/neo4j/2019/09/06/custom-fulltext-analyzer.html)
2. [官方默认支持的Analyzer的代码](https://github.com/neo4j/neo4j/tree/3.5/community/fulltext-index/src/main/java/org/neo4j/kernel/api/impl/fulltext/analyzer/providers)
