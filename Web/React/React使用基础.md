[TOC]

# React使用基础

这里给出使用React的具体过程，通过简单地过程说明，理解使用React的基本步骤，以及相关的操作。

这里给出的方式是从底层一步一步操作的方式，但是真实使用react时，会有一些封装了这个过程的react插件来帮助完成这个过程。

## 1. 安装相应package

cnpm i react react-dom -S

- react：负责创建组件和虚拟DOM，同时管理组件的生命周期；
- react-dom：专门进行DOM操作，最主要的应用场景就是reactDOM.render()，将生成的虚拟DOM放到页面上展示。

## 2. 创建Element并渲染

```js
//必须要这么写
import React from 'react'
import ReactDOM from 'react-dom'

//创建element
/*
参数1：要创建的元素类型，字符串
参数2：一个对象，表示当前DOM元素的属性
参数3：子节点，包括其他虚拟DOM或者文本节点
参数n：其他子节点
*/
const h1 = React.createElement('h1', {id:'h1', titile:'this is h1'}, '这是一个h1')

//渲染到页面上
ReactDOM.render(h1, document.getElementById('app'))
```

注意在上面的步骤中，render方法第二个参数是一个容器，表示要渲染的元素放到哪里。所以还需要做的一步就是在index.html中放入一个id为app的容器。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div id='app'></div>
</body>
</html>
```

## 3. 关于第二步骤的改进

第二个步骤给出了创建DOM并进行渲染的方式，但是用代码创建DOM元素显然是一种很低效的方式，没有直接写HTML方便且直观。

但是在JS中是不支持直接写入HTML的，那怎么办呢？

需要借助于适当的loader来对JS中的HTML标签进行处理，比如使用babel来转换这些JS中的HTML标签。

接下来我们在JS中直接写HTML标签，这种混合有HTML的语法称为JSX语法。JSX名字的含义就是符合XML规范的JS。

JSX的本质就是在运行的时候，会被babel转换为React.createElement的形式来来执行的，相当于多了一层预处理操作。

使用JSX的第一步是干什么呢？安装loader，也就是babel相关的包。

### 3.1 安装babel

- 安装babel插件

**注意：这里babel 7之前的安装方法**
运行：cnpm i babel-core babel-loader babel-plugin-transform-runtime -D
运行：cnpm i babel-preset-env babel-preset-stage-0 -D

- 安装能够识别转换JSX语法的包：babel-preset-react

cnpm i babel-preset-react -D

**babel 7.x使用如下方式替换**

npm i @babel/core @babel/preset-env @babel/preset-react babel-loader @babek/plugin-transform-runtime -D

### 3.2 在webpack.config.js添加配置

由于webpack只能打包后缀为js类型的文件，对于其他类型的文件，比如.png、.jsx、.vue等，是无法主动识别的，这个时候需要第三方的loader。另外，在JS中添加了HTML标签，webpack也是无法处理的，所以webpack此时会去寻找第三方的loader。

配置方法：

```js
const path = require('path')
const HtmlWebPackPlugin = require('html-webpack-plugin')

//创建一个插件实例
const htmlPlugin = new HtmlWebPackPlugin({
    template: path.join(__dirname, './src/index.html'),
    filename: 'index.html'
})

module.exports={
    mode:'development',
    plugins:[
        htmlPlugin
    ],
    module: { //第三方模块的配置规则
        rules: [//第三方匹配规则
            { test: /\.js|jsx$/, use: 'babel-loader', exclude:/node_modules/}, //必须要添加exclude配置项
        ]
    }
}
```

### 3.3 添加.babelrc文件

这个文件是babel的配置文件，在项目的根目录下创建.babelrc文件，这是一个JSON文件，添加如下两项：

```json
{
    "presets":["evn","stage-0","react"],
    "plugins": ["transform-runtime"]
}
```

babel 7之后使用：

```json
{
  "presets": ["@babel/env", "@babel/react"],
  "plugins": ["@babel/transform-runtime"]
}
```

### 3.4 改进后的index.js

```js
console.log('ok')

//必须要这么写
import React from 'react'
import ReactDOM from 'react-dom'

//创建虚拟DOM
// const h1 = React.createElement('h1', {id:'h1', titile:'this is h1'}, '这是一个h1')

const h1 = <h1 id="h1" title="this is h1">这是一个h1</h1>

ReactDOM.render(h1, document.getElementById('app'))
```
