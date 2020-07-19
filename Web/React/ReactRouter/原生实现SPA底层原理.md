[TOC]

# 基于底层原生API实现SPA

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <ul>
      <li><a href="#/home">主页</a></li>
      <li><a href="#/news">新闻</a></li>
      <li><a href="#/profile">个人中心</a></li>
    </ul>
    <div id="container"></div>
  </body>
  <script>
    window.onhashchange = function () {
      var hash = location.hash.substr(2);
      console.log("window.onhashchange -> hash", hash)
      console.log("window.onhashchange -> location", location)
      _html = "";
      if (hash === "home") {
        _html = "主页内容";
      } else if (hash === "news") {
        _html = "新闻内容";
      } else if (hash === "profile") {
        _html = "个人中心";
      }

      document.getElementById("container").innerHTML = _html;
    };
  </script>
</html>
```
