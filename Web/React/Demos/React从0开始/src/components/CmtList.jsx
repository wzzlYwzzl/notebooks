import React from "react";

import CmtItem from "@/components/CmtItem";

import cssobj from "@/css/cmtlist.scss";

// 组件必须继承React.Component
export default class CmtList extends React.Component {
  constructor() {
    super();
    this.state = {
      CommentList: [
        { id: 1, user: "张三", content: "哈哈，沙发" },
        { id: 2, user: "李四", content: "哈哈，板凳" },
        { id: 3, user: "王五", content: "哈哈，凉席" },
        { id: 4, user: "赵六", content: "哈哈，砖头" },
      ],
    };
  }

  render() {
    return (
      <div>
        <h1 className={cssobj.title}>这是评论列表组件</h1>
        {this.state.CommentList.map((item) => (
          <CmtItem {...item} key={item.id}></CmtItem>
        ))}
      </div>
    );
  }
}
