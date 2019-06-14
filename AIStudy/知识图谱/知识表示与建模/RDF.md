[TOC]

# RDF及其扩展

## 参考

1. [w3school RDF](http://www.w3school.com.cn/rdf/rdf_example.asp)

## 1. RDF介绍

RDF(Resource Description Framework)，即资源描述框架。

RDF定义了一种统一的描述资源的方式和规则集，也可以说RDF是一种资源描述模型。

RDF定义资源形式上就是一个SPO三元组，也即Subject-Predicate-Object。RDF只定义了这种主谓宾的大框架，但是对谓语和宾语的具体内容不做限制，可以根据需要选择。

下面是一个描述CD的RDF的例子：

```xml
<?xml version="1.0"?>

<rdf:RDF
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:cd="http://www.recshop.fake/cd#">

<rdf:Description
 rdf:about="http://www.recshop.fake/cd/Empire Burlesque">
  <cd:artist>Bob Dylan</cd:artist>
  <cd:country>USA</cd:country>
  <cd:company>Columbia</cd:company>
  <cd:price>10.90</cd:price>
  <cd:year>1985</cd:year>
</rdf:Description>
<rdf:Description
 rdf:about="http://www.recshop.fake/cd/Hide your heart">
  <cd:artist>Bonnie Tyler</cd:artist>
  <cd:country>UK</cd:country>
  <cd:company>CBS Records</cd:company>
  <cd:price>9.90</cd:price>
  <cd:year>1988</cd:year>
</rdf:Description>
</rdf:RDF>
```

xmlns:rdf 命名空间，规定了带有前缀 rdf 的元素来自命名空间 "http://www.w3.org/1999/02/22-rdf-syntax-ns#"。
xmlns:cd 命名空间，规定了带有前缀 cd 的元素来自命名空间 "http://www.recshop.fake/cd#"。

\<rdf:RDF> 是RDF的根元素，\<rdf:Description>包含了rdf:about描述的资源的属性信息。

元素：\<cd:artist>、\<cd:country>、\<cd:company> 等是此资源的属性。

## 2. RDF序列化方法

RDF定义的是模型，但这些模型以何种方式存储和传输呢？

RDF载体主要有以下方式：RDF/XML，N-Triples，Turtle，RDFa，JSON-LD等几种。

1. RDF/XML
就是用xml来描述RDF数据。之所以用xml描述，是因为xml的技术更为成熟，有很多现成的工具来表示RDF数据。但是xml格式描述RDF太冗长，不便于阅读。所以同常不会用xml来处理RDF数据。

2. N-Triples
即用多个三元组来表示RDF数据，是最直观的一种表示形式。在文件中，每一行表示一个三元组，方便机器解析和处理。开放知识图谱DBpedia通常是用这种格式发布数据的。

3. Turple
使用最多的一种RDF序列化方法，比xml紧凑，且可读性比N-Triples好。

4. RDFa
RDF in Attributes。是HTML5的一个扩展，在不改变任何显示效果的情况下，让网站构建者能够在页面中标记实体。也就是说将RDF嵌入到HTML中，这样可以让浏览器能够更好地从非结构化页面中获取一些有用的结构化信息。可以通过如下链接直观了解这个效果：[rdfa.info](https://rdfa.info/play/)。

5. Json-LD
即Json for Linking Data。可以通过[此网站](https://json-ld.org)具体了解。

## 3. RDFS(RDF Schema)
