[TOC]

# Bazel的Rule

rule是Bazel的关键，是Bazel中真正工作的单元，通过不同的Rule的组合逐步完成代码的编译。

## 1. General Rule

### 1.1 filegroup

用于打包文件，将多个文件打包成一个rule，可供其他rule使用。

### 1.2 config_setting

配置bazel build命令的参数。比如：

```python
config_setting(
    name = "x86_mode",
    values = { "cpu": "x86" }
)
config_setting(
    name = "arm_mode",
    values = { "cpu": "arm" }
)
```

这个表示bazel build可以跟"--cpu x86"或者"--cpu arm"参数。

## 2. embedded non native Rule

### 2.1 http_archive

下载一个bazel repository，然后解压，然后让其可以bind。
