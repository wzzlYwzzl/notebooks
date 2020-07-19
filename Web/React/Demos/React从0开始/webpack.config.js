const path = require("path");
const HtmlWebPackPlugin = require("html-webpack-plugin");

//创建一个插件实例
const htmlPlugin = new HtmlWebPackPlugin({
  template: path.join(__dirname, "./src/index.html"),
  filename: "index.html",
});

module.exports = {
  mode: "development",
  plugins: [htmlPlugin],
  module: {
    //第三方模块的配置规则
    rules: [
      //第三方匹配规则
      { test: /\.js|jsx$/, use: "babel-loader", exclude: /node_modules/ }, //必须要添加exclude配置项
      { test: /\.css$/, use: ["style-loader", "css-loader"] },
      {
        test: /\.scss$/,
        use: [
          "style-loader",
          {
            loader: "css-loader",
            options: {
              modules: { localIdentName: "[path][name]-[local]-[hash:5]" },
            },
          },
          "sass-loader",
        ],
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx", ".json"], //表示这几类文件后缀可以省略
    alias: {
      "@": path.join(__dirname, "./src"),
    },
  },
};
