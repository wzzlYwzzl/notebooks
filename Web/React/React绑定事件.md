[TOC]

# React 绑定事件

React 框架中的事件都是 React 提供的，所以事件的名称不再是传统 HTML 中的事件名称，需要按照 React 的名称规范。比如 onClick、onMouseOver 等，命名规范是小驼峰命名。

添加事件的格式是：`onClick={function}`

比如：

```js
//其中show是一个需要自己定义的函数，注意这种用法是有问题的。
<botton onClick={this.show}>按钮</botton>

// 还有一种常用的形式，通过箭头函数，这种写法是更安全，不易出现问题
// 注意：箭头函数中的this指向的是外部的this，而不是调用者本身的this，这一点很重要
<botton onClick={()=> this.show()}>按钮</botton>
show = () =>{
    console.log('this is show method')
}

```

React 中，如果想要修改 state 中的数据，推荐使用 this.setState({})方法。

## 1. JS中匿名函数

JS中的匿名函数有两种形式：

```js
// 匿名函数形式一
show = function(){
    this.state = {}
}

// 匿名函数形式二
show = () => {
    this.state = {}
}
```

两种匿名函数形式的区别：

- function这种形式的匿名函数中，this指向的是执行这个函数的调用者的this；
- 箭头函数中的this指向的是声明函数时对象的this。
