[TOC]

# cacheout Python library

A caching library for Python.

[Github URL](https://github.com/dgilland/cacheout)

## 特点

1. 基于内存的缓存，后端使用dictionay；
2. 很容易访问的多个缓存对象；
3. 当使用模块级缓存对象，重构运行时的缓存设置；
4. 最大缓存大小限制；
5. 默认缓存时间设置，缓存项自定义存活时间；
6. 批量的设置、获取、删除操作；
7. 线程安全；
8. 多种缓存机制：
   FIFO（现进先出）
   LIFO（后进先出）
   LRU（最近最少使用）
   MRU（最近最多使用）
   LFU（最小频率使用）
   RR（随机替换）

## 要求

python >= 3.4

## 使用方式

参考github链接。
