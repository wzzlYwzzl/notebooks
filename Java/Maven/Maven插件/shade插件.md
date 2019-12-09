[TOC]

# maven-shade-plugin

这个插件的作用就是package，对编译后的java程序打包。和其他打包插件不同的是它会把依赖打包到一个jar包中。除非是这个依赖的scope被设置为test或者provided。比如：

```xml
<dependency>
    <groupId>org.neo4j</groupId>
    <artifactId>neo4j</artifactId>
    <version>${neo4j.version}</version>
    <scope>provided</scope>
</dependency>
```

那么打包的时候，就不会把neo4j这个包以及其相关依赖打包到jar包中。

```xml
​<plugin>
      ​<artifactId>maven-shade-plugin</artifactId>
      ​<executions>
        ​<execution>
          ​<phase>package</phase>
          ​<goals>
            ​<goal>shade</goal>
          ​</goals>
        ​</execution>
      ​</executions>
    ​</plugin>
```

## 参考

1. [官方文档](http://maven.apache.org/plugins/maven-shade-plugin/index.html)
