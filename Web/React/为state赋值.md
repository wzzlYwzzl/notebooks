[TOC]

# React 组件中为 state 赋值

## 1. 一个例子

```js
import React from "react";

export default class BindEvent extends React.Component {
  constructor() {
    super();
    this.state = {
      msg: "yes",
    };
  }

  render() {
    return (
      <div>
        <button onClick={() => show()}></button>
        <h3>{this.state.msg}</h3>
      </div>
    );
  }

  show = () => {
    console.log("this is show method");
    // 这种方式是不对的，页面不会同步渲染
    //this.state.msg = 'no';

    // 这才是正确的方式
    this.setState({ msg: "no" });
  };
}
```

## 2. setState 方式是异步执行的

如果我们在 setState 之后，需要立马使用这个值，如何做呢？

因为 setState 是异步的，所以后面调用取值方法时，获取的值可能不是最新的。

```js
show = () => {
  console.log("this is show method");
  // 这种方式是不对的，页面不会同步渲染
  //this.state.msg = 'no';

  // 这才是正确的方式
  this.setState({ msg: "no" });

  // 这种做法是有问题的，可能获取的值韩式yes
  console.log(this.state.msg);
};
```

正确的做法是在 setState 方法中传入回调函数。

```js
show = () => {
  console.log("this is show method");
  // 这种方式是不对的，页面不会同步渲染
  //this.state.msg = 'no';

  // 这才是正确的方式
  this.setState({ msg: "no" }, function () {
    console.log(this.state.msg);
  });
};
```

## 3. 绑定文本框和 state 中的值

1. 为文本框绑定 onChange 事件函数；
2. 在 onChange 中拿到文本框中的值，有两种方式；
3. onChange 的方法中调用 this.setState 方法对其进行赋值；

```js
<input type="text" style={{width=100%}} value={this.state.msg} onChange={ (e) => {this.changeText(e)}} ref='txt'  />

changeText = (e) => {
    // 获取文本框值的方式一：通过事件参数的方式
    // e就是事件对象，target表示事件相关的DOM元素
    const newValue = e.target.value

    // 获取文本框值的第二种方式：通过DOM元素引用
    // 在DOM中先声明：ref
    const newValue = this.refs.txt.value

    this.setState({
        msg: newValue
    })
}
```
