[TOC]

# REST API

RESTful架构，就是目前非常流行的一种互联网软件架构。

REST 这个词，是Roy Thomas Fielding在他2000年的博士论文中提出的。他这么介绍它写作该论文的目的：

“本文研究计算机科学两大前沿----**软件和网络**----的交叉点。长期以来，**软件研究**主要关注软件设计的分类、设计方法的演化，很少客观地评估不同的设计选择对系统行为的影响。而相反地，**网络研究**主要关注系统之间通信行为的细节、如何改进特定通信机制的表现，常常忽视了一个事实，那就是**改变应用程序的互动风格比改变互动协议，对整体表现有更大的影响**。我这篇文章的写作目的，就是想在符合架构原理的前提下，理解和评估以网络为基础的应用软件的架构设计，得到一个功能强、性能好、适宜通信的架构。”

(This dissertation explores a junction on the frontiers of two research disciplines in computer science: software and networking. Software research has long been concerned with the categorization of software designs and the development of design methodologies, but has rarely been able to objectively evaluate the impact of various design choices on system behavior. Networking research, in contrast, is focused on the details of generic communication behavior between systems and improving the performance of particular communication techniques, often ignoring the fact that changing the interaction style of an application can have more impact on performance than the communication protocols used for that interaction. My work is motivated by the desire to understand and evaluate the architectural design of network-based application software through principled use of architectural constraints, thereby obtaining the functional, performance, and social properties desired of an architecture. )

**PS.** Fielding是一个非常重要的人，他是HTTP协议（1.0版和1.1版）的主要设计者、Apache服务器软件的作者之一、Apache基金会的第一任主席。

Fielding将他对互联网软件的架构原则，定名为REST，即Representational State Transfer的缩写，可以翻译为"表现层状态转化"。

如果一个架构符合**REST原则**，就称它为RESTful架构。

## 1. 几个概念名词

我们先从REST中涉及的基本概念入手，由浅入深，由点到面，逐步深入理解Restful架构的核心思想。

### 1.1 资源(resource)

REST的名称"表现层状态转化"中，省略了主语。"表现层"其实指的是"资源"（Resources）的"表现层"。

资源在REST中是一个比较抽象的词语，用在互联网上就是网络上的一个实体，或者说是网络上的一个具体信息。它可以是一段文本、一张图片、一首歌曲、一种服务，总之就是一个具体的实在。从程序的角度来看就是一个可以用类来描述的东西，都可以称其为资源，资源就是整块的数据。

在RESTful架构中，我们把服务端提供的各种数据都称为资源，每个资源都有URI来与其对应，客户端通过URI来定位资源，然后通过指定URI上的一些Action来操作资源，比如PUT、GET、POST、DELETE、PATCH等等。

编写RESTful API就是为服务端抽象资源，然后构建URL，然后针对URL上的不同动作提供相应的接口。

### 1.2 表现层

"资源"是一种信息实体，它可以有多种外在表现形式。我们把"资源"具体呈现出来的形式，叫做它的"表现层"（Representation）。

比如，文本可以用txt格式表现，也可以用HTML格式、XML格式、JSON格式表现，甚至可以采用二进制格式；图片可以用JPG格式表现，也可以用PNG格式表现。

URI只代表资源的实体，不代表它的形式。严格地说，有些网址最后的".html"后缀名是不必要的，因为这个后缀名表示格式，属于"表现层"范畴，而URI应该只代表"资源"的位置。**它的具体表现形式，应该在HTTP请求的头信息中用Accept和Content-Type字段指定，这两个字段才是对"表现层"的描述**。

表现层就是呈现给用户的信息，前端与后端的交互，前端看到的信息表示表现层，在交互过程中，表现层发生变化。(个人理解)

### 1.3 状态转化(State Transfer)

互联网通信协议HTTP协议，是一个无状态协议。这意味着，所有的状态都保存在服务器端。因此，如果客户端想要操作服务器，必须通过某种手段，让服务器端发生"状态转化"（State Transfer）。而这种转化是建立在表现层之上的，所以就是"表现层状态转化"。

### 1.4 RESTful简单综述

通过前面几个概念的认识，我们对REST规范有了一个初步的认知，按照REST规范的看待数据交互的方式：

- 后端是一堆资源，每个资源都有一个唯一的URI，前端可以通过这个URI来定位自己需要的资源，资源也有粒度的大小；

- 前端负责“表现”这些资源，由于资源的形形色色，所以表现上也就是多种多样，表现层就会随着资源的不同而变化，这称之为“表现层状态转换”；

- 前端借助于HTTP协议提供的GET、UPDATE、PUT、DELETE等来操作底层的资源。

## 2. REST API的优点

要想理解REST API的优点、价值，我们要思考它与HTTP协议是怎样很好地结合的？我们还要思考HTTP协议是如何帮助前后端数据交互的？HTTP相对其他数据传输协议的价值、特点在哪？

在思考这些问题之前，我们先罗列出REST API的一些优点：

- 可以利用缓存Cache来提高响应速度；

- 通讯本身的**无状态性**可以让不同的服务器处理一系列请求中的不同请求，提高服务器的扩展性；

- 浏览器即可做客户端，简化软件开发的需求；

- 相对于其他叠加的HTTP协议之上的机制，REST的软件依赖性更小；

- 不需要额外的资源发现机制；

- 在软件技术演进中的长期的兼容性更好；

### 2.1 关于无状态

所谓无状态即所有的资源都可以URI定位，而且这个定位与其他资源无关，也不会因为其他资源的变化而变化。有状态和无状态的区别，举个例子说明一下，例如要查询员工工资的步骤为第一步：登录系统。第二步：进入查询工资的页面。第三步：搜索该员工。第四步：点击姓名查看工资。这样的操作流程就是有状态的，查询工资的每一个步骤都依赖于前一个步骤，只要前置操作不成功，后续操作就无法执行。如果输入一个URL就可以得到指定员工的工资，则这种情况就是无状态的，因为获取工资不依赖于其他资源或状态，且这种情况下，员工工资是一个资源，由一个URL与之对应可以通过HTTP中的GET方法得到资源，这就是典型的RESTful风格。

## 3. REST API与其他技术对比

REST可以说是一种与DO（分布式对象Distributed Objects）、RPC（远程过程调用Remote Procedure Call）并列的架构体系，是一种设计分布式网络服务或API时遵循的**架构原则以及设计风格**。

### 3.1 REST、DO、RPC之间区别对比

REST | DO | RPC
| - | - | - |
| 核心是资源，按资源建模 | 核心是对象，按对象建模 | 核心是过程，按过程建模
| 中立于开发平台和编程语言多种编程语言实现 | 通常与某种编程语言绑定的，跨语言交互实现复杂 | 虽然应用较广泛，但跨语言交互实现复杂
| 没有统一接口的概念，不同API接口设计风格不同 | 没有统一接口的概念，不同API接口设计风格不同 | 统一接口
| 使用超文本，交互效率比DO更高 | 没有使用超文本，响应的内容中只包含对象本身 | 没有使用超文本，响应的内容中只包含对象本身
| 三种风格中客户端与服务器耦合度最小 | 带来客户端与服务器端的紧耦合。在三种架构风格之中DO风格的耦合度最大的 | 使用了平台中立的消息因而耦合度比DO风格要小，但比REST大
| 支持数据流和管道 | 不支持数据流和管道 | 不支持数据流和管道

### 3.2 REST与CORBA、SNMP、SOAP比较

| | CORBA | SNMP | SOAP | REST
| - | - | - | - | - |
| 架构模式 | 面向对象 | 面向方法 | 面向方法 | 面向资源
| 统一的接口约束 | 无（CORBA服务可以任意添加方法）| 无（可以任意添加方法）| 无（可以任意添加方法） | 有（GET/PUT/POST/DELETE）
| 要求无状态 | 否 | 否 | 否 | 是
| 消息体编码格式(编码效率） | 二进制（高） | 二进制（高） | XML（低） | JSON（中）
| 编译耦合度 | 高（服务端和客户端联动编译） | 低（解耦） | 低（解耦） | 低（解耦）
| 传输协议（效率） | TCP（高） | UDP（高） | HTTP（低） | HTTP（低）
| 在传输协议上封装应用协议 | 是 | 是 | 是 | 否
| 跨语言能力 | 中 | 高 | 高 | 高
| 实现框架 | 重量级 | 轻量级 | 轻量级 | 羽量级
| 是否有归一化的参考实现 | 有 | 有 | 有 | 无
| 原生支持负载均衡 | 否 | 否 | 否 | 是
| 原生支持失效转发 | 否 | 否 | 否 | 是
| 原生支持事件通知 | 是 | 是 | 否 | 否

## 4. REST应用场景

- **适合**
  
  - 无状态的应用 stateless：**判断标准是服务器重启不影响客户端和服务端的交互**。
  
  - 缓存机制有利于解决频繁访问的性能问题。
  
  - 客户端和服务端互相了解。如果服务段是封闭的，并且接口描述是固定并记入合同，SOAP （on WSDL）更合适。
  
  - REST WEB SERVICE更适合对于带宽敏感的应用，适合富客户端。
  
  - 对于需要不断开发新的WEB SERVICE并且需要集成到现有的应用里面，REST WEB SERVICE更合适。对于AJAX的应用，REST WEB SERVICE很容易集成。

- **不适合**

  - 如果软件架构专注于非功能性需求，例如事务，安全性。很多业务超出了简单的CRUD的操作，需要关联上下文以及维护对话状态，这种情况下如果还要用REST，就需要自己额外开发很多辅助功能。
  
  - 异步处理和调用。

## 5. 一个简单的REST例子

1. 获取所有widget

```txt
GET http://example.com/widgets
```

2. 新建一个widget

```txt
POST http://example.com/widgets

data:
name=Foobar
```

3. 查看一个widget

```txt
GET http://example.com/widgets/123
```

4. 更新widget的数据

```txt
PUT http://example.com/widgets/123

data:
name=new name
color=red
```

### 5.1 嵌套资源

有时资源之间存在层级关系，比如一个widget可以被多个user使用，每个用户由可以有不同的sports。那么按照前面的例子会出现下面的URL：

```txt
http://example.com/widgets/123/users
http://example.com/widgets/123/users/333/sports
http://example.com/widgets/123/users/333/sports/567
```

嵌套资源的URL使用方式是没有问题的，但是超过两层其实不是很好的做法了。这时，我们可以用如下形式替换：

```txt
http://example.com/users/333/sports/567
```

**甚至**:

```txt
http://example.com/sports/567
```

### 5.2 REST规范的其他内容

1. 应该将API的版本号放入URL。“GET:[http://www.xxx.com/v1/friend/123]”。或者将版本号放在HTTP头信息中。我个人觉得要不要版本号取决于自己开发团队的习惯和业务的需要，**不是强制的**。

2. URL中**只能有名词而不能有动词**，操作的表达是使用HTTP的动词GET,POST,PUT,DELETEL。URL只标识资源的地址，既然是资源那就是名词了。

3. 如果记录数量很多，服务器不可能都将它们返回给用户。**API应该提供参数，过滤返回结果**。?limit=10：指定返回记录的数量、?page=2&per_page=100：指定第几页，以及每页的记录数。常见的过滤条件如下：

```txt
?limit=10：指定返回记录的数量
?offset=10：指定返回记录的开始位置。
?page=2&per_page=100：指定第几页，以及每页的记录数。
?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
?animal_type_id=1：指定筛选条件
```

参数的设计允许存在冗余，即允许API路径和URL参数偶尔有重复。比如，GET /zoo/ID/animals 与 GET /animals?zoo_id=ID 的含义是相同的。

4. 返回对象

```txt
GET /collection：返回资源对象的列表（数组）
GET /collection/resource：返回单个资源对象
POST /collection：返回新生成的资源对象
PUT /collection/resource：返回完整的资源对象
PATCH /collection/resource：返回完整的资源对象
DELETE /collection/resource：返回一个空文档
```

REST规范要求返回统一的数据格式：

可以按照如下方法，返回Json，包含三个字段：code、message、data。

code是状态码，message是状态码说明信息，data是数据。当code请求成功处理了，返回类似如下的json：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userName": "123456",
    "age": 16,
    "address": "beijing"
  }
}
```

如果失败，则返回类似如下的Json格式：

```json
{
  "code": 401,
  "message": "error  message",
  "data": null
}
```

5. 常用的五个Action

```txt
GET（SELECT）：从服务器取出资源（一项或多项）。
POST（CREATE）：在服务器新建一个资源。
PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
DELETE（DELETE）：从服务器删除资源。
```

例如：

```txt
GET /zoos：列出所有动物园
POST /zoos：新建一个动物园
GET /zoos/ID：获取某个指定动物园的信息
PUT /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
PATCH /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
DELETE /zoos/ID：删除某个动物园
GET /zoos/ID/animals：列出某个指定动物园的所有动物
DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物
```

6. HTTP状态码

1xx：信息
通信传输协议级信息。

2xx：成功
表示客户端的请求已成功接受。

3xx：重定向
表示客户端必须执行一些其他操作才能完成其请求。

4xx：客户端错误
此类错误状态代码指向客户端。

5xx：服务器错误
服务器负责这些错误状态代码。

## 6. RESTful 六大原则

Roy Fielding在论文中阐述了REST架构的六大原则：

### 6.1 C-S架构

数据存储在Server端，Client端负责使用数据。前后端分离，使得client代码的移植性变强，Server端扩展性变强。

### 6.2 无状态

http请求本身就是无状态的，基于C-S架构，客户端的每一次请求带有充分的信息能够让服务端识别。请求所需的一些信息都包含在URL的查询参数、header、div，服务端能够根据请求的各种参数，无需保存客户端的状态，将响应正确返回给客户端。无状态的特征大大提高的服务端的健壮性和可拓展性。

当然，这种无状态性的约束也是有缺点的，客户端的每一次请求都必须带上相同重复的信息确定自己的身份和状态，造成传输数据的冗余性，但这种确定对于性能和使用来说，几乎是忽略不计的。

### 6.3 统一接口

REST架构的核心内容，统一的接口对于RESTful服务非常重要。客户端只需要关注实现接口就可以，接口的可读性加强，使用人员方便调用。

REST接口约束定义为：资源识别; 请求动作; 响应信息; 它表示通过uri标出你要操作的资源，通过请求动作（http method）标识要执行的操作，通过返回的状态码来表示这次请求的执行结果。

### 6.4 一致的数据格式

服务端返回的数据格式要么是XML，要么是Json（获取数据），或者直接返回状态码，一些知名网站的开放平台的操作数据的api，post、put、patch都是返回的一个状态码。

如请求一条微博信息，服务端响应信息应该包含这条微博相关的其他URL，客户端可以进一步利用这些URL发起请求获取感兴趣的信息，再如分页可以从第一页的返回数据中获取下一页的URT也是基于这个原理。

### 6.5 可缓存

在万维网上，客户端可以缓存页面的响应内容。因此响应都应隐式或显式的定义为可缓存的，若不可缓存则要避免客户端在多次请求后用旧数据或脏数据来响应。管理得当的缓存会部分地或完全地除去客户端和服务端之间的交互，进一步改善性能和延展性。

### 6.6 按需编码、可定制代码

服务端可选择临时给客户端下发一些功能代码让客户端来执行，从而定制和扩展客户端的某些功能。比如服务端可以返回一些 Javascript 代码让客户端执行，去实现某些特定的功能。提示：REST架构中的设计准则中，只有按需编码为可选项。如果某个服务违反了其他任意一项准则，严格意思上不能称之为RESTful风格。

## 参考

1. [浅谈REST API](https://blog.csdn.net/champaignwolf/article/details/84099258)
