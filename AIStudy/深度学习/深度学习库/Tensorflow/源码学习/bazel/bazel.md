[TOC]

# bazel

bazel是Google开源的一套编译工具，广泛用于Google内部。Tensorflow项目也是使用Bazel来编译的，所以，要想阅读Tensoflow源码，编译TF源码，bazel是不需要通过的第一关。

## 1. 基本概念

### 1.1 Workspace

一个项目的根目录构成Workspace，一个Workspace中必须包含一个WORKSPACE文件。WORDSPACE文件可以为空，或者包含项目的依赖。

如果一个项目WORKSPACE下面子目录中也包含了WORKSPACE文件，那么Bazel就会在编译的时候忽略这些目录。

### 1.2 repository

代码仓库，代码是通过repository来管理的，可以理解为其他语言中的外部依赖包一样。比如Java中的maven依赖。

### 1.3 package

一个repository中的代码的基本单元是package，一个package是由最相关的一个代码集合及其依赖说明共同组成。

一个package就是一个包含了BUILD或者BUILD.bazel文件的目录，以及不包含BUILD文件的子目录。如果子目录中包含了BUILD，那么这个目录就是一个新的package。

### 1.4 Target

一个package就是一个包含了Target的容器。有三种类型的Target：file、rule、package group。

file：可能是源码source文件，也可能是由source生成的generated文件。

rule：指定如何由一些文件得到另一些文件。输入文件可以是source文件，也可以是generated文件。

### 1.5 Label

每个Target都有一个Label，这个Label就是Target的名字。一个Target只能属于一个Package。

Label的格式：@myrepo//my/app/main:app_binary

同常我们的Label都是同一个repository，所以@myrepo都可以省掉了。

//my/app/main:app_binary是由两部分组成，:前面的部分表示的package，:后面的部分是一个target。

注意：//my/app/main并不表示package下面的所有target，如下两种表示方式是等价的：
//my/app/main
//my/app/main:main

如果target是package内部的，那么可以省略package部分，冒号也是可以省略的，所以如下几种表示是等价的：
//my/app:app
//my/app
:app
app

所以一个package内部的文件同常可以写作相对于package的路径，比如：
generate.cc
testdata/input.txt

### 1.6 Rule

## 2. BUILD文件

每一个package都包含一个package。BUILD是用StarLark语言写的，BUILD文件类似于Python等脚本语言，按照文件中的生命顺序依次执行。

为了清晰的区分代码和数据，BUILD文件中是不允许包含函数的定义、for语句、if语句。这些内容要放到单独的“.bzl”文件中。

### 2.1 BUILD文件的Function

1. export_file

导出一些当前Package的BUILD没有提到的，但是后面会被其他package用到的文件。

## 3. Bazel扩展

Bazel扩展文件都是一个.bzl结尾，通过load方法来加载这些文件中的symbol。例如：
load("//foo/bar:file.bzl", "some_library")

.bzl文件中的以“_”开头的symbol是不能被BUILD导入的。

bzl文件是可以通过load加载其他bzl中的symbol的。

## 4. Dependency

有三种类型的Dependency：srcs、data、deps。

srcs: 依赖的文件

deps: 依赖的其他rule

data: 放的是编译过程中不依赖，但是运行过程时会依赖的内容。可以是文件，也可以是rule。

有时候依赖的是一个目录或者目录的所有文件，那么就需要如下做，在srcs、deps、data下面添加项以“/”或者"/."结尾就可以了。如果是需要监测目录下的文件本身，那么需要使用glob(['directory'])。

## 5. function与rule

function是以def声明定义的，在BUILD中是不能定义函数的。而且*args和**kargs是不允许在BUILD中使用的。
