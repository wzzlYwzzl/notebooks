[TOC]

# Maven使用过程中遇到的问题

## 1. Maven项目引用非Maven的jar包

如果一个jar包不是一个用Maven制作的包，那么如果通过project->properties->Java Build Path->Libraries导入的话，是无法对当前项目用Maven打包的。

这个时候的一个解决方法就是将这个jar包制作为maven包，方法如下：

mvn install:install-file -Dfile=path/to/your/jar -DgroupId=com.baidu -DartifactId=baidu -Dversion=1.0.0 -Dpackaging=jar
