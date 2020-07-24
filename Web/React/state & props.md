[TOC]

# React组件中的数据

在React组件中，存放数据的对象有两个：props和state。关于这两个对象的使用原则：**props是对外的接口，负责获取其他组件传递进来的数据，state是组件的内部状态，组件内部数据可以放到state中。**

## 1. props

在React中，prop（property的简写）是从外部传递给组件的数据，一个React组件通过定义自己能够接受的prop就定义了自己的对外公共接口。

每个React组件都是独立存在的模块，组件之外的一切都是外部世界，外部世界就是通过prop来和组件对话的。

### 1.1 propTypes检查

在ES6方法定义的组件类中，可以通过增加类的propTypes属性来定义prop规格，这不只是声明，而且是一种限制，在运行时和静态代码检查时，都可以根据propTypes判断外部世界是否正确地使用了组件的属性。

比如，对于Counter组件的propTypes定义代码如下：

```js
import PropTypes from 'prop-types'

Counter.propTypes = {
    caption: PropTypes.string.isRequired,
    initValue: PropTypes.number
}
```

propTypes检查只是一个辅助开发的功能，并不会改变组件的行为。

propTypes虽然能够在开发阶段发现代码中的问题，但是放在产品环境中就不大合适了。

首先，定义类的propTypes属性，无疑是要占用一些代码空间，而且propTypes检查也是要消耗CPU计算资源的。

其次，在产品环境下做propTypes检查没有什么帮助，毕竟，propTypes产生的这些错误信息只有开发者才能看得懂，放在产品环境下，在最终用户的浏览器Console中输出这些错误信息没什么意义。

所以，最好的方式是，开发者在代码中定义propTypes，在开发过程中避免犯错，但是在发布产品代码时，用一种自动的方式将propTypes去掉，这样最终部署到产品环境的代码就会更优。现有的babel-react-optimize就具有这个功能，可以通过npm安装，但是应该确保只在发布产品代码时使用它。

### 1.2 属性默认值

前面说了，使用propTypes会对性能有一定的影响，而且如果属性没有声明成isRequired，那么我们后面使用时，就需要在代码中判断属性是否存在。

React为我们提供了一种为属性指定默认值的方式：defaultProps。

比如：

```js
Counter.defaultProps = {
    initValue: 0
}
```

## 2. state

state的修改必须通过setState方法。

## 3. state与props对比

- prop用于定义外部接口，state用于记录内部状态；

- prop的赋值在外部世界使用组件时，state的赋值在组件内部；

- 组件不应该改变prop的值，而state存在的目的就是让组件来改变的。

组件的state，就相当于组件的记忆，其存在意义就是被修改，每一次通过this. setState函数修改state就改变了组件的状态，然后通过渲染过程把这种变化体现出来。

但是，组件是绝不应该去修改传入的props值的。
