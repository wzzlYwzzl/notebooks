[TOC]

# webpack4

由于React开发中使用的是webpack进行打包，所以这里先从0开始展示如何使用webpack4打包一个前端项目。

## 1. 使用webpack4打包项目

1. 创建一个目录，执行npm init -y初始化生成package.json文件；
2. 创建src代码目录、dist产品目录；
3. 在src目录下创建index.html和index.js文件；
4. 安装webpack包：cnpm i webpack webpack-cli -D；

注意：webpack和webpack-cli需要全局安装一份：cnpm i --global webpack webpack-cli。
5. webpack4.x提供约定大于配置的概念，以减少配置。

- 约定打包入口是src->index.js
- 打包输出文件dist->main.js
- 4.x新增mode选项，取值包括：development和production

6. 安装webpack-dev-server以实现实时打包:

- cnpm i webpack-dev-server -D
- 在package.json的scripts中添加“"dev":"webpack-dev-server"”。

7. 为了能够直接在浏览器中访问html文件，而不是访问项目的根目录，可以使用另一个插件：html-webpack-plugin。

- 安装：cnpm i html-webpack-plugin -D
- 配置：需要在webpack.config.js中导入插件

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
    ]
}
```

## 2. webpack配置根目录

有时我们会在代码中看到别人在引入组件时会如下写：

```js
import Hello from '@/components/Hello'
```

那这个@是什么含义呢？

其实@就是一个别名，这个别名在webpack.config.js中配置的：

```js
const path = require("path");
const HtmlWebPackPlugin = require("html-webpack-plugin");

//创建一个插件实例
const htmlPlugin = new HtmlWebPackPlugin({
  template: path.join(__dirname, "./src/index.html"),
  filename: "index.html",
});

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
  resolve: {
    extensions: [".js", ".jsx", ".json"], //表示这几类文件后缀可以省略
    alias: {
      "@": path.join(__dirname, "./src"), //这里就是配置@别名的
    },
  },
};
```
