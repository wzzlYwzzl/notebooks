[TOC]

# LDA之Python应用举例

## 1. 操作过程

下面的例子以英文文档为例。

### 1.1 准备文档集合

```python
doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."

doc_complete = [doc1, doc2, doc3, doc4, doc5]
```

### 1.2 数据清洗和预处理

```python
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer //词标准化，将不同词性的词统一
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

# 每个doc会被分词，由于是英文，所以分词就是以空格分割
doc_clean = [clean(doc).split() for doc in doc_complete] 
```

## 1.3 准备Document-Term矩阵

```python
import genism
from gensim import corpora

# 创建语料的词语词典，每个单独的词语都会被赋予一个索引
dictionary = corpora.Dictionary(doc_clean)

# 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
```

## 1.4 构建LDA模型

```python
# 使用 gensim 来创建 LDA 模型对象
Lda = genism.models.ldamodel.LdaModel

# 在 DT 矩阵上运行和训练 LDA 模型
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
```

## 1.5 输出结果

```python
# 输出结果
print(ldamodel.print_topics(num_topics=3, num_words=3))

[
    '0.168*health + 0.083*sugar + 0.072*bad,
    '0.061*consume + 0.050*drive + 0.050*sister,
    '0.049*pressur + 0.049*father + 0.049*sister
]
```

每一行包含了主题词和主题词的权重，Topic 1 可以看作为“不良健康习惯”，Topic 3 可以看作 “家庭”。

## 参考

1. [主题模型 LDA 入门（附 Python 代码）](https://blog.csdn.net/selinda001/article/details/80446766)

