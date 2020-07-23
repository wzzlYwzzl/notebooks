[TOC]

# React-Redux

Redux是“React全家桶”中的一个重要成员，它试图为React应用提供`可预测化的状态管理`机制。

Redux可以和多种框架结合，和React结合需要借助于react-redux工具。

react-redux提供了两个重要的对象：Provider和connect，前者使React组件可以被连接，后者则是把React组件和Redux的store真的连接起来。

## 1. 准备工作

```js
const reducer = (state = {count:0}, action) => {
    switch (action.type) {
        case 'INCREASE': return {count: state.count + 1};
        case 'DECREASE': return {count: state.count - 1};
        default: return state;
    }
}

const actions = {
    increate: () => ({type: 'INCREASE'}),
    decrease: () => ({type: 'DECREASE'})
}

const store = createStore(reducer);

store.subcribe(() => console.log(store.getState()))

store.dispatch(actions.increase())
store.dispatch(actions.increase())
store.dispatch(actions.increase())
```

我们在store上，通过dispatch发射一个action，store内的数据就会相应发生变化。

当然，我们可以直接在React中使用Redux：在最外层容器组件中初始化store，然后将state上的属性作为props层层传递下去。

```js
class App extends Component {
    componentWillMount() {
        store.subscribe((state) => this.setState(state))
    }

    render() {
        return (
            <Comp
                state={this.state}
                onIncrease={()=>store.dispatch(actions.increase())}
                onDecrease={()=>store.dispatch(actions.decrease())}
            />
        )
    }
}
```

也可以如下做：

- 在入口index.js文件中初始化store，并export出去，然后import到定义组件的文件中去。

上面提到的两种方法不是最佳的方式，最好的方式就是使用react-redux提供的Provider和connect方法。

## 2. 使用react-redux

首先在最外层容器中，把所有的容器都包裹在Provider组件中，并将之前创建的store作为prop传给Provider。

```js
const App = () => {
    return (
        <Provider> store=(store)>
            <Comp />
        </Provider>
    )
}
```

Provider内的任何一个组件，比如这里的Comp，如果需要使用state中的数据，就必须是被“connect”处理过的组件。

```js
class MyComp extends Component {
    // 组件内容
}

const Comp = connect(...args)(MyComp)
```

## 3. connect

connect的函数签名如下：

```js
connect([mapStateToProps], [mapDispatchToProps], [mergeProps],[options])
```

接下来我们介绍这四个参数：

### 3.1 mapStateToProps

```js
mapStateToProps(state, ownProps): stateProps
```

这个函数的作用就是将state中的数据作为props绑定到组件上。

比如：

```js
const mapStateToProps = (state) => {
    return {
        count: state.count
    }
}
```

**这个函数的第一个参数就是Redux的store**，我们从中获取count属性，**因为返回了具有count属性的对象，所以MyComp会有名为count的props字段**。

```js
class MyComp extends Component {
    render() {
        return <div>计数：{this.props.count}</div>
    }
}

const Comp = connect(...args)(MyComp)
```

当然，你没有必要将state中的数据原封不动地传入组件，可以根据state中的数据，动态地输出组件需要的最小属性。

```js
const mapStateToProps = (state) => {
    return {
        greaterThanFive: state.count > 5,
    }
}
```

**函数的第二个参数ownProps**，是MyComp自己的props。有时候，ownProps也会对其产生影响。比如在store中维护了一个用户列表，而你的组件MyComp只关心一个用户，可以通过props中的userId体现。

```js
const mapStateToProps = (state, ownProps) => {
    return {
        user: _.find(state.userList, {id: ownProps.userId})
    }
}

class MyComp extends Component {
    static PropTypes = {
        userId: PropTypes.string.isRequied,
        user: PropTypes.object
    };

    render() {
        return <div>用户名：{this.props.user.name}</div>
    }
}

const Comp = connect(mapStateToProps)(MyComp)
```

**当state变化时，或者ownProps变化时**，mapStateToProps都会被调用，计算出新的stateProps，在于ownProps merge后，更新给MyComp。

这就是Redux store中的数据连接到组件的基本方式。

**注：**

- 什么是“MyComp自己的props”？
  假设在不使用react-redux的时候，MyComp的父组件是ParentComp，那么上文中的ownProps是ParentComp传递给MyComp的全部属性。

- mapStateToProps为MyComp添加的属性，不可能被方法mapDispatchToProps访问到，反之亦然。

- 如果使用PropTypes对MyComp做属性类型检查，那么两个方法为MyComp添加的属性是存在的。

### 3.2 mapDispatchToProps

```js
mapDispatchToProps(dispatch, ownProps): dispatchProps
```

connect第二个参数的作用就是**将action作为props**绑定到组件上。

```js
const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    increase: (...args) => dispatch(actions.increase(...args)),
    decrease: (...args) => dispatch(actions.decrease(...args))
  }
}

class MyComp extends Component {
  render(){
    const {count, increase, decrease} = this.props;
    return (<div>
      <div>计数：{this.props.count}次</div>
      <button onClick={increase}>增加</button>
      <button onClick={decrease}>减少</button>
    </div>)
  }
}

const Comp = connect(mapStateToProps， mapDispatchToProps)(MyComp);
```

由于mapDispatchToProps方法返回了具有increase属性和decrease属性的对象，这两个属性也会成为MyComp的props。

如上所示，调用actions.increase()只能得到一个action对象{type:'INCREASE'}，要触发这个action必须在store上调用dispatch方法。

dispatch正是mapDispatchToProps的第一个参数。但是，**为了不让 MyComp 组件感知到dispatch的存在，我们需要将increase和decrease两个函数包装一下，使之成为直接可被调用的函数**（即，调用该方法就会触发dispatch）。

Redux 本身提供了bindActionCreators函数，来将action包装成直接可被调用的函数。

```js
import {bindActionCreators} from 'redux';

const mapDispatchToProps = (dispatch, ownProps) => {
  return bindActionCreators({
    increase: action.increase,
    decrease: action.decrease
  });
}
```

同样，**当ownProps变化的时候，该函数也会被调用，生成一个新的dispatchProps**，（在与stateProps和ownProps merge 后）更新给MyComp。注意，**action的变化不会引起上述过程，默认action在组件的生命周期中是固定的**。

**转载注：**

- 函数connect甚至react-redux的核心在于：将 Redux 中 store 的 state 绑定到组件的属性上，使得对 state 的修改能够直接体现为组件外观的更改。因此，参数mapStateToProps是非常重要的，但是参数mapDispatchToProps则比较多余——因为简单粗暴地导入全局 store 同样能达到相同的目的（事实上笔者就是这么做的）。

### 3.3 mergeProps

```js
[mergeProps(stateProps, dispatchProps, ownProps): props]
```

之前说过，不管是stateProps还是dispatchProps，都需要和ownProps merge 之后才会被赋给MyComp。connect的第三个参数就是用来做这件事。通常情况下，你可以不传这个参数，connect就会使用Object.assign替代该方法。

### 3.4 其他

最后还有一个options选项，比较简单，基本上也不大会用到（尤其是你遵循了其他的一些 React 的「最佳实践」的时候），本文就略过了。希望了解的同学可以直接看文档。

## 参考

1. [React 实践心得：react-redux 之 connect 方法详解](https://segmentfault.com/a/1190000015042646)
