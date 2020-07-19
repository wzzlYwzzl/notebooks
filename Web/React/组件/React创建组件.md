[TOC]

# React创建组件

React有两种创建组件的方式。

## 1. 第一种创建组件方式

```jsx
//必须要这么写
import React from "react";
import ReactDOM from "react-dom";

// 第一种创建组件的方式
// 函数首字母必须大写,组件也必须返回一个JSX虚拟DOM元素
function Hello() {
    return <div>这是一个hello</div>
}

ReactDOM.render(
  <div>
    123
    {/*这里就是使用自定义组件的方式*/}
    <Hello></Hello>
  </div>,
  document.getElementById("app")
);
```

如果我们需要为组件传递属性，类似于HTML标签的属性，可以如下写：

```jsx
//必须要这么写
import React from "react";
import ReactDOM from "react-dom";

// 第一种创建组件的方式
// 函数首字母必须大写,组件也必须返回一个JSX虚拟DOM元素
// 函数可以通过一个参数来接受组件的属性信息
function Hello(props) {
    //props是只读的，不能重新赋值
    console.log(props)
    return <div>这是一个hello----{props.name}</div>
}

const dog = {
    name:'大黄',
    age:3,
    gender:'雄'
}

ReactDOM.render(
  <div>
    123
    <Hello name={dog.name} age={dog.age}></Hello>
  </div>,
  document.getElementById("app")
);
```

传递属性方式的优化，上面的例子中dog有三个属性，我们是展开传递的，但是如果属性多了，这么传递其实就很麻烦了，所以可以用下面的方式传递一个对象的所有属性：

```jsx
const dog = {
    name:'大黄',
    age:3,
    gender:'雄'
}

ReactDOM.render(
  <div>
    123
    {/*这种方式传递dog的所有属性，三个点是ES6中的展开运算符，展开对象获取所有属性*/}
    <Hello {...dog}></Hello>
  </div>,
  document.getElementById("app")
```

### 1.1 将组建放到一个单独的文件

为了方便的管理组建，让代码更有条理，我们通常会把组件单独放到一个文件中。下面我们把上面使用的Hello组件放到单独文件中。

1. 在src目录下面创建components目录；
2. 在components目录下创建Hello.jsx文件，然后添加如下内容：

```jsx
//注意这个是必须引入的
import React from 'react'

// 第一种创建组件的方式
// 函数首字母必须大写,组件也必须返回一个JSX虚拟DOM元素

//这是第一种到处Hello组件的方式，这样外部才能使用
// export default function Hello(props) {
function Hello(props) {
    //props是只读的，不能重新赋值
    console.log(props)
    return <div>这是一个hello----{props.name}</div>
}

//这是第二种到处组件的方式
export default Hello
```

### 1.2 在其他程序中使用组件

我们上面单独创建了组件，接下来我们在index.js文件中使用上面的组件。

```jsx

//第一种引入方式，如果没有在webpack.config.js中配置相应的内容，则需要添加文件后缀
import Hello from './components/Hello.jsx'

//如果在webpack.config.js中配置了，那么可以省略文件后缀，怎么配置呢？下面介绍。
import Hello from '@/components/Hello'
```

在webpack.config.js中添加如下配置：

```js
module.exports = {
  mode: "development",
  plugins: [htmlPlugin],
  module: {
    //第三方模块的配置规则
    rules: [
      //第三方匹配规则
      { test: /\.js|jsx$/, use: "babel-loader", exclude: /node_modules/ }, //必须要添加exclude配置项
    ],
  },
  //下面的内容就是解决进入组件时不添加后缀的方式
  resolve: {
    extensions: [".js", ".jsx", ".json"], //表示这几类文件后缀可以省略
     alias: {
      "@": path.join(__dirname, "./src"), //这里就是配置@别名的
    },
  },
};
```

## 2. 第二种创建组件的方式

使用class关键字创建，class是ES6的特性。

### 2.1 class关键字介绍

下面对比就的function方式和新的class关键字方式创建类的方法。

```js
// class关键字是实现面向对象的新形式

// 这是旧的创建对象的形式
function Person(name, age) {
  this.name = name;
  this.age = age;
}

//静态属性
Person.info = 'info'

// 实例方法
Person.prototype.say = function(params) {
    console.log('hello')
}

// 定义静态方法
Person.show = function(params) {
    console.log('这是静态方法')
}


// class 花括号内只能写静态方法、方法、构造器
// class 类似个语法糖，内部实现还是之前的配方
class Animal {
  // 每一个类中都有一个构造器
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  // 静态属性
  static info = "abc"

  jiao(){
      console.log("这是实例方法")
  }

  static show(){
      console.log("这是静态方法")
  }
}
```

### 2.2 class 继承

继承就是使用extends关键字，和Java相似。

```js
class Person {
    constructor(name, age){
        this.name = name
        this.age = age
    }

    sayHello(){
        console.log("hello")
    }
}

class Chinese extends Person {
    constructor(name, age){
        super(name, age) // 优先调用super()
    }
}
```

### 2.3 使用class方式创建组件

```js
import React from "react";

// 组件必须继承React.Component
export default class ClassHello extends React.Component {
  constructor() {
    super()
    // 这里的属性是可写的
    this.state = {
        msg: '这是组件的数据消息'
    }
  }

  // class关键字创建的组件，需要使用外部传递的属性，不需要接受，直接通过this.props使用
  // 这里的props也是只读的，和function方式创建的一样
  // 组件内必须有一个render方法，这个方法返回一个JSX虚拟DOM对象
  render() {
  return <div>ClassHello 组件 -- {this.props.name} -- {this.state.msg}</div>;
  }
}

// 这种方式也是可以的
//export default ClassHello
```

## 3 class方式和function方式对比

1. class方式创建的组件有自己的私有数据（this.state）和生命周期函数；

2. function创建的组件只有props，没有自己的私有数据和生命周期函数；

3. 用class创建的组件是有状态组件，function方式创建的组件是无状态组件，无状态组件用的不多。

4. 无状态组件比有状态组件效率高。

5. 组件中的props和state之间有什么区别？
   - props是外部传递的数据；
   - state是组件私有的数据，一般通过ajax获取，或者是私有内部数据；
   - state中的数据是可读写的；
