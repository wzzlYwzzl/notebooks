[TOC]

# Xml解析

Xml解析有两种方式：DOM和SAX。

## 1. DOM解析方式

DOM，文件对象模型，是W3C的标准，提供有标准的解析方式。

DOM解析方式是把整个XML加载到内存，适用于XML随机访问，缺点是占用内存比较大。

### JAVA中DOM解析的框架

- JAXP
- JDOM
- DOM4j

## 2. SAX解析方式

Simple API for XML。

事件驱动型的XML解析方式，顺序读取，逐行扫描，不用一次装载整个文件，遇到标签会触发一个事件，适合于XML的顺序访问，占用内存资源稍小。

### JAVA中SAX解析工具

- Sax
- digester3
