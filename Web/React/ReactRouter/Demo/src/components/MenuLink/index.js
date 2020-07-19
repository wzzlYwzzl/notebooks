// 这个组件用于模拟 NavLink的功能
// 这里利用了children的特性
// 功能：返回一个Link，由于组件简单不需要内部状态，使用函数组件

import React from "react";
import { Link, Route } from "react-router-dom";

export default function MenuLink(props) {
  return (
    <Route
      path={props.to}
      children={({match}) => {
        return <Link className={match ? 'active': ''} to={props.to}>{props.label}</Link>;
      }}
    />
  );
}
