[TOC]

# JSX

JSX的语法本质：并不是把JSX直接渲染到页面上，而是先内部转换为createElement的形式，在渲染的。

## 1. JSX基础语法

### 1.1 JSX中混合写入js表达式

在JSX中插入js表达式，只需要将相应表达式放到大括号{}之间即可。

- 渲染数字
- 渲染字符串
- 渲染布尔值
- 为属性绑定值
- 渲染jsx元素
- 渲染jsx元素数组
- 将普通字符串转为jsx数组并渲染到页面

```js
import React from 'react'
import ReactDOM from 'react-dom'

let a = 10;
let str = "你好，中国";
let bool = true;
let title = "ooo";

const h1 = <h1>这是一个h1</h1>;

const arr = [<h1>this is h1</h1>, <h2>this is h2</h2>, <h3>this is h3</h3>];

const arrStr = ["毛利兰", "柯南", "小五郎", "灰原衰"];

//定义一个空数组，将用来存放名称标签
//注意：react中需要把key添加给foreach或map或for循环控制的东西
const nameArr = [];
arrStr.forEach((item) => {
  const temp = <h4 key={item}>{item}</h4>;
  nameArr.push(temp);
});

ReactDOM.render(
  <div>
    {a + 1}
    <hr />
    {str}
    <hr />
    {bool ? "is true" : "is false"}
    <hr />
    <p title={title}>这是p标签</p>
    <hr />
    {h1}
    {/* {arr} */}
    <hr />
    {nameArr}
    <hr />
    {arrStr.map((item) => (
      <h4 key={item}>{item}</h4>
    ))}
  </div>,
  document.getElementById("app")
);

```

### 1.2 JSX中的注释

```jsx
{/*注释内容*/}
```

### 1.3 注意事项

- jsx中为元素添加class类型，需要使用className来替代class；
- jsx中要用htmlFor替换label的for属性；
- jsx创建DOM时，所有节点必须有为一个的根元素进行包裹；
- jsx语法中，标签必须成对出现，如果出现单标签，也必须自闭合；
