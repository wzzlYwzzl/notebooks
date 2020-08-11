[TOC]

# go modules

Go modules 是 Go 语言自 1.11 版本推出的一个依赖版本控制工具，从 1.14 版本开始，便可用于生产环境。Go 官方也推荐通过 go modules 来进行版本依赖管理。

## 1. go 版本管理历史

在介绍 go modules 之前，我们先简单介绍一下 golang 进行版本管理的发展历程。在 go modules 出来之前，go 的版本管理一直被大众所诟病，先后经历了多个版本管理方式的进化：

- 1.5 版本之前，没有版本管理的概念，所有的代码都放到 GOPATH 目录下，GOPATH 就是一个代码仓库，但是问题在于它不支持版本控制，如果项目 A 和项目 B 依赖于同一个模块的不同版本，如果这个模块不同版本之间不存在兼容问题，那么就会导致冲突问题。

- 1.5 之后，推出了 vendor 机制。所谓 ventor，就是项目目录下面有一个 vendor 目录，里面放了项目依赖的一些 package，当执行 go build 时，会优先从 vendor 目录下面查找相应的依赖，如果没有找到，在从 GOPATH 目录下面查找。

- 1.9 版本推出了实验性质的 dep 机制。

- 1.11 版本，退出 go modules 机制，modules 机制的原型是 vgo。

## 2. GOPATH 模式

GOPATH 是一个环境变量，它指向的是整个 go 项目的根目录，GOPATH 目录下一共包含了三个子目录，分别是：

- bin：存储所编译生成的二进制文件。

- pkg：存储预编译的目标文件，以加快程序的后续编译速度。

- src：存储所有.go 文件或源代码。在编写 Go 应用程序，程序包和库时，一般会以\$GOPATH/src/github.com/\*\*/\*\*的路径进行存放。

在使用 GOPATH 模式下，我们需要将应用代码存放在固定的$GOPATH/src目录下，并且如果执行go get来拉取外部依赖会自动下载并安装到$GOPATH 目录下。

## 3. go modules 的基本使用

### 3.1 环境变量配置

Go1.13 新增了 go env -w 用于写入环境变量，而写入的地方是 os.UserConfigDir 所返回的路径，需要注意的是 go env -w 不会覆写。需要指出，它不会覆盖系统环境变量。

需要配置的环境变量主要有两个：GO111MODULE 和 GOPROXY。

```shell
#打开 Go modules
go env -w GO111MODULE=on
#设置 GOPROXY
go env -w GOPROXY=https://goproxy.cn,direct
```

### 3.2 初始化项目目录

```shell
go mod init demo
```

执行完上面的命令，会得到一个 go.mod 文件，里面内容如下：

```shell
module demo

go 1.13
```

### 3.3 创建 main.go

```go
package main

import (
    "github.com/gin-gonic/gin"
    "fmt"
)

func main() {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        fmt.Println("hello world!")
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })
    r.Run() // listen and serve on 0.0.0.0:8080
}
```

### 3.4 go build

执行完 go build 得到如下内容：

```shell
├── demo
├── go.mod
├── go.sum
└── main.go
```

项目中增加了 go.sum 和 demo 可执行文件。

go.sum 文件中的内容如下：

```shell
github.com/davecgh/go-spew v1.1.0/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
github.com/davecgh/go-spew v1.1.1/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
github.com/gin-contrib/sse v0.1.0 h1:Y/yl/+YNO8GZSjAhjMsSuLt29uWRFHdHYUb5lYOV9qE=
github.com/gin-contrib/sse v0.1.0/go.mod h1:RHrZQHXnP2xjPF+u1gW/2HnVO7nvIa9PG3Gm+fLHvGI=
...
```

go.mod 中的内容变成如下：

```shell
module demo

go 1.13

require github.com/gin-gonic/gin v1.6.3
```

## 4. go modules 相关环境变量说明

```shell
$ go env
GO111MODULE="auto"
GOPROXY="https://proxy.golang.org,direct"
GONOPROXY=""
GOSUMDB="sum.golang.org"
GONOSUMDB=""
GOPRIVATE=""
...
```

### 4.1 GO111MODULE

Go 语言提供了 GO111MODULE 这个环境变量来作为 Go modules 的开关，其允许设置以下参数：

auto：只要项目包含了 go.mod 文件的话启用 Go modules，目前在 Go1.11 至 Go1.14 中仍然是默认值。

on：启用 Go modules，推荐设置，将会是未来版本中的默认值。

off：禁用 Go modules，不推荐设置。

### 4.2 GOPROXY

这个环境变量主要是用于设置 Go 模块代理（Go module proxy），其作用是用于使 Go 在后续拉取模块版本时能够脱离传统的 VCS 方式，直接通过镜像站点来快速拉取。

GOPROXY 的默认值是：https://proxy.golang.org,direct，这有一个很严重的问题，就是 proxy.golang.org 在国内是无法访问的，因此这会直接卡住你的第一步，所以你必须在开启 Go modules 的时，同时设置国内的 Go 模块代理，执行如下命令：

```shell
go env -w GOPROXY=https://goproxy.cn,direct
```

GOPROXY 的值是一个以英文逗号 “,” 分割的 Go 模块代理列表，允许设置多个模块代理，假设你不想使用，也可以将其设置为 “off” ，这将会禁止 Go 在后续操作中使用任何 Go 模块代理。

**direct 是什么**

实际上 “direct” 是一个特殊指示符，用于指示 Go 回源到模块版本的源地址去抓取（比如 GitHub 等），场景如下：当值列表中上一个 Go 模块代理返回 404 或 410 错误时，Go 自动尝试列表中的下一个，遇见 “direct” 时回源，也就是回到源地址去抓取，而遇见 EOF 时终止并抛出类似 “invalid version: unknown revision...” 的错误。

### 4.3 GOSUMDB

它的值是一个 Go checksum database，用于在拉取模块版本时（无论是从源站拉取还是通过 Go module proxy 拉取）保证拉取到的模块版本数据未经过篡改，若发现不一致，也就是可能存在篡改，将会立即中止。

GOSUMDB 的默认值为：sum.golang.org，在国内也是无法访问的，但是 GOSUMDB 可以被 Go 模块代理所代理（详见：Proxying a Checksum Database）。

因此我们可以通过设置 GOPROXY 来解决，而先前我们所设置的模块代理 goproxy.cn 就能支持代理 sum.golang.org，所以这一个问题在设置 GOPROXY 后，你可以不需要过度关心。

另外若对 GOSUMDB 的值有自定义需求，其支持如下格式：

格式 1：<SUMDB_NAME>+<PUBLIC_KEY>。

格式 2：<SUMDB_NAME>+<PUBLIC_KEY> <SUMDB_URL>。

也可以将其设置为“off”，也就是禁止 Go 在后续操作中校验模块版本。

### 4.4 GONOPROXY/GONOSUMDB/GOPRIVATE

这三个环境变量都是用在当前项目依赖了私有模块，例如像是你公司的私有 git 仓库，又或是 github 中的私有库，都是属于私有模块，都是要进行设置的，否则会拉取失败。

更细致来讲，就是依赖了由 GOPROXY 指定的 Go 模块代理或由 GOSUMDB 指定 Go checksum database 都无法访问到的模块时的场景。

而一般建议直接设置 GOPRIVATE，它的值将作为 GONOPROXY 和 GONOSUMDB 的默认值，所以建议的最佳姿势是直接使用 GOPRIVATE。

并且它们的值都是一个以英文逗号 “,” 分割的模块路径前缀，也就是可以设置多个，例如：

```shell
go env -w GOPRIVATE="git.example.com,github.com/eddycjy/mquote"
```

设置后，前缀为 git.example.com 和 github.com/eddycjy/mquote 的模块都会被认为是私有模块。

如果不想每次都重新设置，我们也可以利用通配符，例如：

```shell
go env -w GOPRIVATE="*.example.com"
```

这样子设置的话，所有模块路径为 example.com 的子域名（例如：git.example.com）都将不经过 Go module proxy 和 Go checksum database，需要注意的是不包括 example.com 本身。

## 5. go mod 相关命令

- go mod download 下载 go.mod 文件中指明的所有依赖

- go mod tidy 整理现有的依赖，删除未使用的依赖。

- go mod graph 查看现有的依赖结构

- go mod init 生成 go.mod 文件 (Go 1.13 中唯一一个可以生成 go.mod 文件的子命令)

- go mod edit 编辑 go.mod 文件

- go mod vendor 导出现有的所有依赖 (事实上 Go modules 正在淡化 Vendor 的概念)

- go mod verify 校验一个模块是否被篡改过

- go clean -modcache 清理所有已缓存的模块版本数据。

- go mod 查看所有 go mod 的使用命令。

## 6. 用 go get 拉取新的依赖

- 拉取最新的版本(优先择取 tag)：go get golang.org/x/text@latest

- 拉取 master 分支的最新 commit：go get golang.org/x/text@master

- 拉取 tag 为 v0.3.2 的 commit：go get golang.org/x/text@v0.3.2

- 拉取 hash 为 342b231 的 commit，最终会被转换为 v0.3.2：go get golang.org/x/text@342b2e

- 用 go get -u 更新现有的依赖
