[TOC]

# Linux磁盘分区、挂载

如果系统新增加了一块硬盘，那么我们要想使用它，需要经过三个步骤：分区、创建文件系统和挂载。

## 1. 分区

Linux分区有两个常用工具：fdisk、parted。fdisk针对MBR模式进行分区，parted针对GPT模式分区，当然parted也支持MBR模式分区。

PS. 如果单个分区超过2T，就需要使用GPT模式进行分区。

### 1.1 fdisk分区

- fdisk -l
查看磁盘信息

- fdisk /dev/sdb
对/dev/sdb进行分区

### 1.2 parted分区

具体操作方法参考[1][3][4]。

**警告处理：**
"The resulting partition is not properly aligned for best performance"

解决办法参考[2]中提到的simple way，其中提到的核心就是使用“mkpart LVM ext4 0% 100%”，使用百分比。

## 参考

1. [fdisk与parted分区](https://www.cnblogs.com/hfjiang/p/10276985.html)
2. [GNU Parted: Solving the dreaded "The resulting partition is not properly aligned for best performance"](https://blog.hqcodeshop.fi/archives/273-GNU-Parted-Solving-the-dreaded-The-resulting-partition-is-not-properly-aligned-for-best-performance.html)
3. [Linux分区之parted命令](https://www.cnblogs.com/Cherry-Linux/p/10103172.html)
4. [parted分区命令](https://www.cnblogs.com/pipci/p/11372530.html)
