[TOC]

# Deepdive通用特征库：ddlib

Deepdive提供了Python代码编写的一个通用特征提取库ddlib，它的作用就是为mention和relation创建与具体应用和业务无关的通用特征。这些特征可以保证获取基本的mention和relation提取的质量。

ddlib通用特征库需要利用NLP标注结果，比如分词结果、词性标注、命名实体识别次序列标注、依存路径等等。

通用特征库也可以指定词典，这些词典中的词是我们认为有助于我们进行的关系提取。ddlib会根据这个词典来创建额外的特征。

## 1. 通用特征

关于mention和relations通用特征包含两类，不同的特征使用不同的前缀来描述。

### 1.1 关于mention的特征

1. 组成mention的单词的词性标注集合，前缀**POS_SEQ**。
2. 组成mention的NER标注标签集合，前缀**NER_SEQ**。
3. 组成mention的lemmas，即词目集合，前缀**LEMMA_SEQ**。
4. 组成mention的words的结合，前缀**WORD_SEQ**。
5. 组成mention的words的长度的s和，前缀**LENGTH**。
6. mention的第一个单词是否是以大写字母开始，**STARTS_WITH_CAPITAL**。
7. mention左右两侧的lemmas、NER序列特征，左侧、右侧两个窗口各三个，2 \* 3 \* 3，共18个特征。以**W**开头。
8. mention是否出现在用户指定的dictionary中，前缀**IN_DICT**。
9. 包含mention的句子中是否包含用户指定关键词，前缀**KW_IND**。
10. 同一个句子中，mention和用户指定的关键词之间的最短依存路径。前缀***KW*。

### 1.2 关于relation的特征

除了单独指出的，其他前缀和上面的介绍一样：

1. 同一relation的mention之间的词性标签集合。
2. 同一relation的mention之间的NER标签集合。
3. 同一relation的mention之间的lemmas集合。
4. 同一relation的mention之间的words集合。
5. mentions之间的单词的长度之和。
6. mentions是否一个大写字母开头。
7. mention之间的words、NER标签的1~3 n-gram信息，前缀***NGRAM*。
8. ...

## 2. 加载用户词典

通过加载用户指定的包含领域知识的词典，来引入新的特征。

词典文件的格式：一行一个关键词；

加载方式：

```python
import ddlib

ddlib.load_dictionary("file.txt", dict_id="dic_id")
```
