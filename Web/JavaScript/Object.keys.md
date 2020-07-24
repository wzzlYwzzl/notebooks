[TOC]

# JavaScript Object.keys()方法

Object.keys 返回一个所有元素为**字符串的数组**，其元素来自于从给定的 object 上面**可直接枚举的属性**。这些属性的顺序与手动遍历该对象属性时的一致。

这里面有一个核心的概念：**属性可枚举性**。那么什么属性可以枚举呢？

## 1. 属性可枚举性

对象的属性是否具有可枚举属性是由 enumerable 值决定；

- 可以通过 obj.propertyIsEnumerable(prop)；来判断 obj 对象的 prop 属性是否能够枚举，该方法返回的是一个布尔值。

- js 中基本包装类型的原型属性是不可枚举的，如 Object, Array, Number。

- 可枚举的属性可以通过for...in循环进行遍历（除非该属性名是一个Symbol），或者通过Object.keys()方法返回一个可枚举属性的数组。

- 对于通过直接的赋值和属性初始化的属性，该标识值默认为即为 true。但是对于通过 Object.defineProperty 等定义的属性，该标识值默认为 false。

不可枚举属性虽然不能为遍历工具所遍历，但是仍旧可以读取：

```js
function Person() {
    this.name = "Ykx";
};
let ykx = new Person();
Object.defineProperty(ykx, "sex", {
    value: "male",
    //是否为枚举属性
    enumerable: false
});
Object.getOwnPropertyNames(ykx).forEach(function(key) {
    console.log(key)//name ,sex
});
```

### 1.1 for ... in 与 Object.keys() 与 getOwnPropertyNames三者的区别

1. **for ... in**

遍历对象的每一个可枚举属性,包括原型链上面的可枚举属性(js基本包装类型的原型属性是不能被遍历因为是不可枚举的)。

```js
function Person() {
    this.name = "Ykx";
};
Person.prototype.School = 'Tust';
Object.defineProperty(ykx, "sex", {
    value: "male",
    //是否为枚举属性
    enumerable: false
});
let ykx = new Person();

for(var p in ykx){
　　console.log(p); //name，School
}
```

2. **Object.keys()**

Object.keys方法只能遍历**自己的对象上的可枚举的属性**，不能遍历自己原型上可枚举的属性。

```js
function Person() {
    this.name = "Ykx";
};
Person.prototype.School = 'Tust';
Object.defineProperty(ykx, "sex", {
    value: "male",
    //是否为枚举属性
    enumerable: false
});
let ykx = new Person();
Object.keys(ykx).forEach(function(key) {
    console.log(key) //name
});
```

3. **Object.getOwnPropertyNames()**

```js
function Person() {
    this.name = "Ykx";
};
Person.prototype.School = 'Tust';
Object.defineProperty(ykx, "sex", {
    value: "male",
    //是否为枚举属性
    enumerable: false
});
let ykx = new Person();
Object.getOwnPropertyNames(ykx).forEach(function(key) {
    console.log(key);//name,sex
});
```

上面的例子打印出来了name和sex,说明它**遍历自身对象的所有属性**，**包括可枚举不可枚举**，但是**原型上的属性是无法遍历的**。

4. JSON.stringify

这个方法也只能读取对象本身的可枚举属性，并序列化为JSON对象。

![1](./images/object.keys/1.png)
