[TOC]

# SpringMVC

在[MVC](./MVC.md)中介绍了MVC这种设计模式，SpringMVC就是在Spring的基础上实现的基于MVC模式的Spring模块，它是一个Web框架。

## 1. SpringMVC工作流程

SpringMVC框架由DispatcherServlet、HandlerMapping、Controller、ViewResolver、View等组成。工作原理如下图：

![1](./images/springmvc-1.png)

工作流程如下：

1. 客户端请求提交到**DispatcherServlet**。
2. 由DispatcherServlet控制器寻找一个或多个**HandlerMapping**，找到处理请求的Controller。
3. DispatcherServlet将请求提交到**Controller**。
4. Controller调用业务逻辑xxxService处理后返回ModelAndView。
5. DispatcherServlet寻找一个或多个**ViewResolver**视图解析器，找到ModelAndView指定的视图。
6. View负责将结果显示到客户端。

宏观而言，DispatcherServlet是整个Web服务的控制器。微观上讲，Controller是单个Http请求处理的Controller。ModelAndView则是请求过程中返回的Model和View。

## SpringMVC常用注解

- @Controller
负责注册一个bean 到spring 上下文中

- @RequestMapping
注解为控制器指定可以处理哪些 URL 请求

- @RequestBody
该注解用于读取Request请求的body部分数据，使用系统默认配置的HttpMessageConverter进行解析，然后把相应的数据绑定到要返回的对象上 ,再把HttpMessageConverter返回的对象数据绑定到 controller中方法的参数上

- @ResponseBody
该注解用于将Controller的方法返回的对象，通过适当的HttpMessageConverter转换为指定格式后，写入到Response对象的body数据区

- @ModelAttribute
在方法定义上使用 @ModelAttribute 注解：Spring MVC 在调用目标处理方法前，会先逐个调用在方法级上标注了@ModelAttribute 的方法。在方法的入参前使用 @ModelAttribute 注解：可以从隐含对象中获取隐含的模型数据中获取对象，再将请求参数 –绑定到对象中，再传入入参将方法入参对象添加到模型中

- @RequestParam
在处理方法入参处使用 @RequestParam 可以把请求参 数传递给请求方法

- @PathVariable
绑定URL占位符到入参

- @ExceptionHandler
注解到方法上，出现异常时会执行该方法

- @ControllerAdvice
使一个Contoller成为全局的异常处理类，类中用
@ExceptionHandler方法注解的方法可以处理所有Controller发生的异常

## 参考

1. [Spring MVC框架入门教程](http://c.biancheng.net/spring_mvc/)
2. [SpringMVC框架介绍](https://blog.csdn.net/number_oneengineer/article/details/82775419)
