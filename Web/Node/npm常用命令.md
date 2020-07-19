[TOC]

# npm常用命令

## 1. npm install

npm install 简写为 npm i

--save 可简写为 -S
--save-dev 简写为 -D

npm run start 简写为 npm start

### 1.1 --save-dev

npm i --save-dev package

表示是工程构建时的依赖，比如常见的：webpack、bebel-loader、less-loader等。

### 1.2 --save

npm i --save package

项目运行时需要的依赖，这些依赖在发布时会一起发布。

### 1.3 说明

运行上面两个命令安装的依赖包会写入package.json中的：devDependencies和dependencies中。
