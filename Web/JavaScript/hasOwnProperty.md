[TOC]

# hasOwnProperty

此方法用于检测一个对象是否含有指定的**自身属性**，即这个属性不是通过继承获得的。

## for...in中添加if(obj.hasOwnProperty(attr))

for...in 循环会遍历所有可枚举属性，加上hasOwnProperty()方法，可以忽略掉继承属性，这样就能确保遍历的是Obj的可枚举的自身属性。

适用于：含有继承属性的对象，也就是除了Object的所有对象。

```js
function foo() {  
  this.name = 'foo'
  this.sayHi = function () {
     console.log('Say Hi')
  }
}

foo.prototype.sayGoodBy = function () {  
  console.log('Say Good By')
}

let myPro = new foo()
console.log(myPro.name) // foo
console.log(myPro.hasOwnProperty('name')) // true
console.log(myPro.hasOwnProperty('toString')) // false
console.log(myPro.hasOwnProperty('hasOwnProperty')) // fasle
console.log(myPro.hasOwnProperty('sayHi')) // true
console.log(myPro.hasOwnProperty('sayGoodBy')) // false
console.log('sayGoodBy' in myPro) // true
```

## 为什么有的地方用Object.prototype.hasOwnProperty.call(obj，name)

Javascript 并没有保护 hasOwnProperty 为关键字或保留字。因此，会有这样一种情况：对象自己改写了hasOwnProperty方法，比如下面代码中该方法永远返回false。如果另一个不知情的人使用了foo，并想通过foo.hasOwnProperty判断foo是否含有某个属性时就会永远返回false，这显然是有问题的。

这时候可以借助于Object.prototype.hasOwnProperty或{}.hasOwnProperty来判断对象是否含有某个非继承属性。

适用于：不确定Object类型变量是否改写了hasOwnProperty的情况

```js
var foo = {
  hasOwnProperty: function() {
    return false;
  },
  bar: 'Here be dragons'
};

foo.hasOwnProperty('bar'); // 总是返回 false
// 使用另一个 hasOwnProperty 并将 this 设置为 foo 来调用它
{}.hasOwnProperty.call(foo, 'bar'); // true
```
