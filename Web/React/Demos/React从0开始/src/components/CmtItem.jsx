import React from "react";

import cssobj from '@/css/cmtitem.scss'

function CmtItem(props) {
  return (
    <div className={cssobj.cmtbox}>
      <h1 className={cssobj.title}>评论人：{props.user}</h1>
      <p>评论内容：{props.content}</p>
    </div>
  );
}

export default CmtItem;
