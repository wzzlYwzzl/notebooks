import React, { Component } from "react";

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  NavLink,
  Redirect,
} from "react-router-dom";

import "./css/index.css";

import Home from "./components/Home";
import News from "./components/News";
import Profile from "./components/Profile";
import MenuLink from "./components/MenuLink";
import NotFound from "./components/NotFound";

class App extends Component {
  render() {
    return (
      <Router>
        <div>
          <h1>react路由</h1>
          {/* 声明式的路由，还有一种是编程式的路由 */}
          {/* 通过将Link替换为NavLink，然后添加activeClassName，再在css中添加样式，实现点击链接之后变颜色 */}
          <NavLink to="/home" activeClassName="selected">
            首页
          </NavLink>{" "}
          <br />
          <NavLink to="/news" activeClassName="selected">
            新闻
          </NavLink>{" "}
          <br />
          <NavLink to="/profile" activeClassName="selected">
            个人中心
          </NavLink>{" "}
          <br />
          {/*使用route定义path与组件映射关系，其中path表示要跳转的路径，
          component表示要显示的组件、页面，下面注释的部分给出了一种写法。
          这两种写的的区别类似于编程时写多个if和使用if...else...的区别。
          */}
          {/* <Route path="/home" component={Home} />
          <Route path="/news" component={News} />
          <Route path="/profile" component={Profile} /> */}
          <Switch>
            <Route path="/home">
              <Home />
            </Route>
            <Route path="/news">
              <News />
            </Route>
            <Route path="/profile">
              <Profile />
            </Route>
            <Route
              path="/renders"
              render={(props) => {
                // 当使用router进行SPA开发时，无论是函数组件还是类组件，props中都被添加一些额外的信息
                // 1. history属性，可用于做函数式导航
                // 2. location包含url地址信息
                // 3. match路由传参时使用，比如/news/14
                console.log("App -> render -> props", props);
                return (
                  <div>
                    <h2>render函数式组件的渲染</h2>
                  </div>
                );
              }}
            ></Route>
            <Route path='/notfound'>
              {/* 这里是用来处理无效页面请求的一种方式 */}
              <NotFound />
            </Route>
            
            {/* 通过重定向来处理错误请求 */}
            <Redirect from='*' to="/notfound" />
            
          </Switch>
          <hr />
          <MenuLink to="/home" label="首页" /> <br />
          <MenuLink to="/news" label="新闻" /> <br />
          <MenuLink to="/profile" label="个人中心" />
        </div>
      </Router>
    );
  }
}

export default App;
