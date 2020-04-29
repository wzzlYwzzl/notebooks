[TOC]

# REfO

REfO，Regular Expressions for Objects，是一个Python库，功能和re正则表达式模块类似，但是区别在于REfO用于处理的不是字符序列，而是对象序列，可以理解为它是re的超集。通过写对象的正则表达式，支持匹配对象序列。

比如我们常见的正则表达式是“[abc]+|ef*”，等等这种pattern用来匹配字符串。

REfO的正则表达式的形式是，比如传统形式“a*”，对应的REfO形式为Star(Literal("a"))，一个稍微复杂的形式是：

"(ab)+|(bb)*?" 对应REfO为:

a = Literal("a")
b = Literal("b")
regex = Plus(a + b) | Star(b + b, greedy=False)。

[REfO的Github项目](https://github.com/machinalis/refo)