[TOC]

# React Router

React Router 是第三方为 React 开发 SPA(Single Page Application)开发出来的库。

优先建议阅读[官方文档](https://reactrouter.com/web)学习内容。

## 1. 关于 SPA

SPA，在一个页面内完成所有功能，但是并不是一次性全部显示所有内容。那底层是如何实现在不同操作、不同时间显示不同内容的呢？

实现方法（用到比较多的是锚点和 h5 history）：

1. 锚点(hash)
   window.onhashchange，只要 windows 的 hash 值发生变化，就会发生刷新。

2. h5(history)

还可以用以下技术实现：

3. ajax
   问题是不能有历史记录。

4. iframe 框架
   - seo 不友好；
   - 操作不方便；
   - 最新的 HTML5 建议框架集废除；

## 2. 使用 React Router 步骤

1. create-react-app demo-app

2. cnpm i react-router-dom

3. 引入依赖

```js
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
```

下面介绍上面引入的内容的含义：

- BrowserRouter

路由容器，所有的路由操作都必须定义在该组件下面。

除了 BrowserRouter，还有一种 HashRouter。

开发阶段，可以使用 HashRouter，可以很方便看出页面是有 hash 跳转，但是不利于 SEO。对于搜索引擎而言，hash不是一个新的url地址不会收录。

上线后建议使用 BrowserRouter，url是pathinfo，这种路由地址更加利于 SEO。

- Route

路线，该组件定义路径和显示组件的对应关系。

- Link

说白了就是一个 a 链接，实现声明式跳转。

4. 创建路由表

所有与路由有关的内容都要放到 `<Router></Router>`标签内。

路由表是通过：

```html
<Route path='' component={}></Route>
```

来完成的。

下面给出官方的一个简单例子：

```js
import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

export default function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/about">About</Link>
            </li>
            <li>
              <Link to="/users">Users</Link>
            </li>
          </ul>
        </nav>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/users">
            <Users />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>About</h2>;
}

function Users() {
  return <h2>Users</h2>;
}
```

## 3. 路由嵌套

给出官方的例子：

```js
import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

export default function App() {
  return (
    <Router>
      <div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/about">About</Link>
          </li>
          <li>
            <Link to="/topics">Topics</Link>
          </li>
        </ul>

        <Switch>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/topics">
            <Topics />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>About</h2>;
}

function Topics() {
  let match = useRouteMatch();

  return (
    <div>
      <h2>Topics</h2>

      <ul>
        <li>
          <Link to={`${match.url}/components`}>Components</Link>
        </li>
        <li>
          <Link to={`${match.url}/props-v-state`}>
            Props v. State
          </Link>
        </li>
      </ul>

      {/* The Topics page has its own <Switch> with more routes
          that build on the /topics URL path. You can think of the
          2nd <Route> here as an "index" page for all topics, or
          the page that is shown when no topic is selected */}
      <Switch>
        <Route path={`${match.path}/:topicId`}>
          <Topic />
        </Route>
        <Route path={match.path}>
          <h3>Please select a topic.</h3>
        </Route>
      </Switch>
    </div>
  );
}

function Topic() {
  let { topicId } = useParams();
  return <h3>Requested topic ID: {topicId}</h3>;
}
```

## 4. 编程式导航

方法就是通过获取props中的history对象，然后在里面添加要跳转的路径即可。

```js
import { useHistory } from "react-router-dom";

function HomeButton() {
  let history = useHistory();

  function handleClick() {
    // 这里push还可以添加另一个参数，它
    // 是一个对象，里面添加各种属性信息，这个属性信息会被传到新的页面组件的state内。
    // 第二个参数的一种用处就是比如用户操作订单页面，但是没有登录，此时需要跳转到登录界面，但是登录之后，为了更好地用户体验，需要返回到订单界面，此时需要将跳转前的页面信息保存到第二个参数中。
    history.push("/home");
  }

  return (
    <button type="button" onClick={handleClick}>
      Go home
    </button>
  );
}
```

