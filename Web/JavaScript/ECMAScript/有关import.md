[TOC]

# ES 中有关 import

我们在写 JS 代码时，会遇到两种 import 形式：

```js
import React from "react";
import { Link } from "react-router-dom";
```

那么什么时候需要带{}，什么时候不带{}呢？

**如果是用 export default 导出的，那么久不用加{}，如果是用 export 导出的，那么就需要使用{}**。

## 1. 关于 export 与 export default

在JavaScript ES6中，export与export default均可用于导出常量、函数、文件、模块等，你可以在其它文件或模块中通过import+(常量 | 函数 | 文件 | 模块)名的方式，将其导入，以便能够对其进行使用，但在一个文件或模块中，export、import可以有多个，export default仅有一个。

1.export与export default均可用于导出常量、函数、文件、模块等

2.在一个文件或模块中，export  、import可以有多个，export default仅有一个

3.通过export方式导出，在导入时要加{ }，export default则不需要

4.export能直接导出变量表达式，export default不行
