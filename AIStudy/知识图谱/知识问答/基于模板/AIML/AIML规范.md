[TOC]

# AIML规范

AIML1.0是Richard S. Wallace博士1995-2000年之间设计出来的。除了标准的tag之外，它还有一些其他系统添加的扩展。

## 1. AIML 1.0.1 Tags

- aiml
- bot
- category
- condition
- formal
- gender
- get
- id
- input
- li
- lowercase
- pattern
- person
- person2
- random
- set
- sr
- srai
- star
- template
- that
- thatstar
- think
- topic
- topicstar
- uppercase

AIML1.0.1 Pandora Tags extention

- date
- request
- response
- learn
- eval

## 2. AIML2.0 Tags

Tag | AIML1.0 | AIML2.0
:-: | :-: | :-:
aiml | 有 | 有 |
bot | 有 | 有 |
category | 有 | 有 |
condition | 有 | 有 |
date | 扩展 | 有 |
denormalize | 无 | 有 |
eval | 扩展 | 有 |
explode | 无 | 有 |
first | 无 | 有 |
formal | 有 | 有 |
gender | 有 | 有 |
get | 有 | 有 |
id | 有 | 有 |
input | 有 | 有 |
interval | 无 | 有 |
learn | 扩展 | 有 |
li | 有 | 有 |
loop | 无 | 有 |
lowercase | 有 | 有 |
map | 无 | 有 |
normalize | 无 | 有 |
pattern | 有 | 有 |
person | 有 | 有 |
person2 | 有 | 有 |
program | 无 | 有 |
random | 有 | 有 |
request | 扩展 | 有 |
rest | 无 | 有 |
sentence | 无 | 有 |
set | 有 | 有 |
size | 无 | 有 |
sr | 有 | 有 |
star | 有 | 有 |
system | 无 | 有 |
template | 有 | 有 |
that | 有 | 有 |
thatstar | 有 | 有 |
think | 有 | 有 |
topic | 有 | 有 |
topicstar | 有 | 有 |
uppercase | 有 | 有 |
vocabulary | 无 | 有 |

Pandora在AIML2.0上增加的Tag

- addtriple
- deletetriple
- learnf
- select
- tuple
- uniq
- search
- sraix

**Program-y**在上面所有Tag基础上又增加的Tag：

- log
- iset
- authorise
- extension
- resetlearn
- resetlearnf

## 3. AIML Tags介绍

AIML中的tag，有的是用于category中的pattern，有的是用于category的template。

### 3.1 Pattern Matching

#### 3.1.1 Priority Matching

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>HELLO $FRIEND #</pattern>
        <template>Hi there, friend!</template>
    </category>

    <category>
        <pattern>HELLO #</pattern>
        <template>Hi there!</template>
    </category>
</aiml>
```

上面这个例子实现的就是hello + 0或任意个单词的回答。但是对于hello friend有一个特殊的回答，希望优先匹配这个特殊的回答，那么就需要“$”这个优先符，有了它，就会优先匹配相应的pattern。

ps. program-y的解析顺序是：**priority->"#"->"_"->word->"^"->"*"**，所以如果把第二个pattern的“hello #”替换为“hello *”会看不出优先级的作用。

“$”符号的使用方式就是把其放到需要优先关注的单词或中文字的前面。

#### 3.1.2 0 or more Matching

匹配0个或者多个单词或字。对应的占位符：# 或 ^。

为什么会有两个呢？

因为是优先级考虑，**priority->"#"->"_"->word->"^"->"*"**，我们发现匹配“0 or more”和“1 or more”的占位符的优先级是交叉的，可以做到两种占位符任一个优先匹配。

#### 3.1.3 1 or more Matching

匹配一个或者多个英文单词或者中文字。对应的占位符：* 或 _。

#### 3.1.4 set Matching

```xml
<category>
    <pattern> I LIKE THE COLOR <set name="colors" /></pattern>
    <template>
        That is great, I like that color too.
    </template>
</category>
```

set是一个类别词的集合。在pattern中只要匹配了set对应类别的词，那么就表示匹配了这个pattern。

比如上面的例子中，colors只是类别，与这个colors类别相关的词汇存在一个文件中。以program-y的用法为例，说明如何使用set。

1. 在配置文件的storage配置section中，需要配置两个地方：sets和sets_storage。这个配置说明的是set相关配置的目录；
2. 在这个目录中放一个colors.txt文件，文件名大小写不敏感，然后在colors.txt文件中放属于colors的单词。注意：这文件中的单词可以是多个词的单词。

#### 3.1.5 iset Matching

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern><iset words="HELLO, HI, YO" /> THERE</pattern>
        <template>Hi there!</template>
    </category>
</aiml>
```

iset是set的inline版本，如果只有少数的单词构成的set，那么没有必要单独构建一个set文件来存储这些内容，这个时候可以使用iset。

iset的多个词汇之间用逗号隔开。

#### 3.1.6 bot Matching

一个聊天机器人对应一个bot，一个bot自身有很多自己的虚拟的拟人属性，比如说性别、身高、居住地等等。

这些属性会在配置文件的“properties_storage”配置项中指定。这个文件中放了很多key:value的kv对来描述bot。这些bot属性是可以在AIML中使用的。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>WHAT IS YOUR NAME</pattern>
        <template>My name is <bot name="name" /></template>
    </category>
    <category>
        <pattern>ARE YOU A MAN OR A WOMAN</pattern>
        <template>I am considered <bot name="gender" /> by many</template>
    </category>
</aiml>
```

上面这个例子中，使用了bot的两个属性：name和gender。

#### 3.1.7 regex Matching

基于正则表达式的匹配。这是program-y中引入的tag，并非aiml2.0的标准tag。

**注意**：正则表达式对单个word进行匹配检查。在中文情况下，单个word其实就是指单个中文字符，如果是非中文字符，那么它们会被连在一起(以空格为分割)作为一个单词，比如数字，英文单词。目前正则表达式只适合于英文和数字的场景，中文并不适合。

正则表达式有两种使用方式：pattern方式和template方式。

pattern方式就是将正则表达式直接写到aiml中，比如：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>I LIKE THE <regex pattern="COL[O|OU]R" /> RED</pattern>
        <template>Wow, I like red too!</template>
    </category>
</aiml>
```

template方式是将正则表达式写到配置文件中，格式是name:pattern，在配置文件中有一个配置项“regex_storage”来指定这个配置文件。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>I LIKE THE <regex template="colour-spelling" /> RED</pattern>
        <template>Wow, I like red too!</template>
    </category>
</aiml>
```

上面这个例子中，需要在regex配置文件中添加：colour-spelling:COL[O|OU]R，效果是和上面的pattern一样的。

#### 3.1.8 star Matching

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>I LIKE THE COLOR *</pattern>
        <template>I LIKE <star /> TOO </template>
    </category>
</aiml>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>MY FIRST NAME IS * AND MY SURNAME IS *</pattern>
        <template>NICE TO MEET YOU <star index="1"/> <star index="2" /></template>
    <category>
</aiml>
```

**注意**：这里有一个理解上的陷阱，虽然这里的tag关键字是star，但是并不表示这里只能匹配pattern中的"*"，它可以匹配前面提到的七种：\* , _ , ^, #, set, iset, bot, regex。

#### 3.1.9 处理优先级

$  Priority
\#   0 or more
_   1 or more
word
set
iset
bot
regex
word
^   0 or more
\*   1 or more

#### 3.1.10 topic tag

topic是为了解决同一个问题在不同上下文中会有不同的回答这个问题的。不同的上下文这里是通过一个topic变量来表示的，它是内置的。当匹配pattern时，会把上下文的topic也添加到要匹配的字符串中。只有topic同时匹配时，才是最终的问题答案。

如何设置topic呢？

在template中通过set tag来设置。比如：

```xml
<template>
<think><set name="topic">fishing</set></think>
</template>
```

上面的例子会设置一个全局变量：topic，其值为"fishing"。

#### 3.1.11 that tag

that标签也是对pattern的一种补充。that也是上下文约束的一种方式，但是这个约束和topic约束主题不一样，它约束的是前一个问题的答案。这样的约束是为了保证answer的连贯性。

```xml
<category>
    <pattern>PLEASE GO ON</pattern>
    <that>ELIZA FOR PRESIDENT</that>
    <template>
        She is old enough, because she was born in 1966. And she was born in the U.S.
    </template>
</category>
```

上面这个例子：当用户前面问了一个问题，答案是“Eliza for president”，那么当用户接着说：“please go on”，那么就可以如下回答。

### 3.2 template Tag

接下来介绍在category中的\<template>标签包含的Tag。

#### 3.2.1 addtriple、deletetriple、select、uniq、search

这几个tag都是和RDF相关的操作，前两个是增删操作，后三个是查询操作。

```xml
<category>
    <pattern>* is a *</pattern>
    <template>
        <addtriple>
            <subj><star /></star>
            <pred>isA</pred>
            <obj><star index="2"/></obj>
        </addtriple>
    </template>
</category>
```

作用很直白，就是在KB中添加三元组。与其对应的另外一个tag是：deletetriple。

```xml
<category>
    <pattern>REMOVE * IS A * </pattern>
    <template>
        <deletetriple>
            <subj><star /></star>
            <pred>isA</pred>
            <obj><star index="2"/></obj>
        </deletetriple>
    </template>
</category>
```

```xml
<category>
    <pattern>HOW MANY LEGS DOES A MONKEY HAVE</pattern>
    <template>
        <uniq>
            <subj>MONKEY</subj>
            <pred>legs</pred>
            <obj>?legs</obj>
        </uniq>
    </template>
</category>
```

```xml
<select>
    <vars>?x ?y</vars>
    <q><subj>?x</subj><pred>legs</pred><obj>?y</obj></q>
</select>
```

#### 3.2.2 authorise

权限判断的tag。

#### 3.2.3 condition

1. Block condition
   满足条件就返回对应的值。下面四种形式是等价的，都是property的值为v时，满足条件返回X。

   类似于编程语言中的：if condition return value

```xml
<condition name="property" value="v">X</condition>

<condition name="property"><value>v</value>X</condition>

<condition value="v"><name>property</name>X</condition>

<condition><name>property</name><value>v</value>X</condition>
```

2. single-predicate condition
   多个条件判断，满足一个就返回对应的值，不再检查。这种condition类似于编程语言中的if...elif..elif..else

```xml
<condition name="property">
    <li value="a">X</li>
    <li value="b">Y</li>
    <li>Z</li> <!-- Optional default value if no condition met -->
</condition>
```

3. multi-predicate condition
   检测每一个li，只要有一个满足，就这直接返回结果。这里和上面不一样的是这里的li之间是不存在排他关系的。

```xml
<condition>
    <li name='1' value="a">X</li>
    <li value="b"><name>1</name>Y</li>
    <li name="1"><value>b</value>Z</li>
    <li><name>1</name><value>b</value>Z</li>
    <li>Z<l/i><!-- Optional default value if no condition met -->
</condition>
```

4. looping

#### 3.2.4 date & interval

```xml
<category>
    <pattern>WHAT IS THE DATE</pattern>
    <template>
        Today is <date format="%B %d, %Y" />
    </template>
</category>

<category>
    <pattern>WHAT IS THE DATE</pattern>
    <template>
        Today is <date><format>%B %d, %Y</format></date>
    </template>
</category>
```

interval返回两个date或者time之间的差值。

```xml
<category>
    <pattern>AGE IN YEARS</pattern>
    <template>
        <interval format="%B %d, %Y">
            <style>years</style>
            <from><bot name="birthdate"/></from>
            <to><date format="%B %d, %Y" /></to>
        </interval>
    </template>
</category>
```

#### 3.2.5 eval & learn & learnf

eval的作用就是返回其包含的tag经过分析得到的值。

比如下面的例子中，eval就是执行所包含的\<get>tag的结果，也就是里面变量的内容。

```xml
<category>
    <pattern>REMEMBER * IS MY PET *</pattern>
    <template>
    <learn>
      <think>
          <set var="name"><star /></set>
          <set var="animal"><star index="2" /></set>
      </think>
      <category>
        <pattern>WHO IS
            <eval>
                <get var="name"/>
            </eval>
        </pattern>
        <template>
            Your
            <eval>
                <get var="animal"/>
            </eval>.
        </template>
      </category>
    </learn>
  </template>
</category>
```

learn允许从pattern中学习新的知识。learn标签中的内容用于表示新学习到的category。

learnf相比learn的作用就是会把学到的内容持久化，服务重启之后就会直接拥有这些知识。learn则只有在相应pattern匹配过后

#### 3.2.6 normalize & denormalize

normalize是将字符串中包含的特殊字符转换为内部的表示。denormalize则是逆过程，将中间的表示形式转换为answer中合理的展示形式。

比如：
normalize中：
you'll转换为you will

在denormalize中，则要反向转换。

```xml
<category>
    <pattern>MY EMAIL ADDRESS IS *</pattern>
    <template>
        Your email address is stored as <normalize><star /><normalize>
    </template>
</category>

<category>
    <pattern>MY EMAIL ADDRESS IS *</pattern>
    <template>
        Your email address is stored as <normalize />
    </template>
</category>
```

#### 3.2.7 explode & implode

expode将字符串转换为单个字符分开的形式。比如：hello经过explode之后是“h e l l o”。

implode则是将匹配的字符串除去其中的空格进行拼接。

#### 3.2.8 first & rest

first返回单词列表的首个。比如：“I am a boy”，经过first返回的是“I”。

```xml
<category>
    <pattern>MY NAME IS * </pattern>
    <template>
        Your first name is <first><star /></star>
    </template>
</category>
```

rest则是返回除了第一个word之外的其他words。还是字符串“I am a boy”，rest返回的是“am a boy”。

#### 3.2.9 extention

extention可以理解为一种调用内部python逻辑的一种方式。

比如：

```xml
<category>
    <pattern>
        BANK BALANCE *
    </pattern>
    <template>
        <srai>
            SHOW_BALANCE
            <extension path="programy.extensions.banking.balance.BankingBalanceExtension">
                <star />
            </extension>
        </srai>
    </template>
</category>
```

上面的例子中，会将*匹配的内容传递给“programy.extensions.banking.balance.BankingBalanceExtension”类的excute方法中。

#### 3.2.10 formal

对字符串的每个word首字母大写处理。

```xml
<category>
    <pattern>MY NAME IS * * </pattern>
    <template>
        Hello Mr <formal><star /></formal> <formal><star index="2"/></formal>
    </template>
</category>
```

#### 3.2.11 gender

对指定的文本进行性别转换。其实本质上还是一种mapping。

在program-y中，由gender_storage配置项指定配置文件。

#### 3.2.12 get & set

获取变量值和设置变量值。

```xml
<!-- Access Global Variable -->
<category>
    <pattern>USER COUNT</pattern>
    <template>
        Total active users is <get name="activeusers" />
    </template>
</category>

<!-- Access Local Variable -->
<category>
    <pattern>QUESTION COUNT</pattern>
    <template>
        You have asked <get var="questioncount" /> questions in this conversation.
    </template>
</category>
```

#### 3.2.13 id

获取bot的名字。

#### 3.2.14 input

返回用户的整个问题。

```xml
<category>
    <pattern>What was my question</pattern>
    <template>
        You question was <input />
    </template>
</category>
```

#### 3.2.15 log

作用就是允许在AIML文件中输出日志信息。

```xml
<category>
    <pattern>HELLO *</pattern>
    <template>
        <log>You said hello</log>
    </template>
</category>

<category>
    <pattern>Goodbye *</pattern>
    <template>
        <log level="error">You said goodbye</log>
    </template>
</category>
```

#### 3.2.16 lowercase & uppercase

对匹配的内容进行大小写转换。

```xml
<category>
    <pattern>HELLO *</pattern>
    <template>
        <lowercase />
    </template>
</category>
```

#### 3.2.17 map

```xml
<category>
    <pattern>WHAT NOISE DOES A * MAKE</pattern>
    <template>
       A <star/> says <map name="animalsounds"><star /></map>
    </template>
</category>
```

map中的name="name"，冒号中的name必须是文件的名称，map的配置在program-y中也是由map_storage配置项指定的。

#### 3.2.18 oob

oob可以理解为AIML中提供功能扩展的部分，用它可以实现更为复杂的功能。和extention有点类似，但是oob可以解析AIML中的xml块，所以可以处理更加复杂的结构。

```xml
<oob>
    <email>
        <to>recipient</to>
        <subject>subject text</subject>
        <body>body text</body>
    </email>
</oob>
```

关于program-y中oob如何使用，参考：[如何创建自己的OOB](https://github.com/keiffster/program-y/wiki/OOB)
