[TOC]

# Lucene Analyzer

## Analyzer哪个阶段起作用

## 几个重要的概念

1. Tokenizer
将char序列生成一个个的token，token就是比如一个单词等，一个token，会被用于构建索引。

2. Analyzer
用于构建TokenStream。一个Analyzer代表了一种构建索引的策略。

3. TokenStream
TokenStream有两种：Tokenizer和TokenFilter。

4. TokenFilter
输入是token，对token进行加工处理，得到新的token。

## 自定义Analyzer
