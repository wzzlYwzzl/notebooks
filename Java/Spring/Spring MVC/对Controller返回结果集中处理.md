[TOC]

# 集中处理Controller返回结果

先描述一下要解决的问题：

我们写controller时，需要将controller的结果包装成统一的类返回给前端，这会带来很多的重复操作，比如在每个controller代码中都会有类似下面的代码：

```java
Response resp = new Response()
resp.setPropertyA(***)
resp.setPropertyB(***)
```

为了避免这种重复的代码，可以用下面的方法解决。

## 1. 实现ResponseBodyAdvice接口

```java
@ControllerAdvice
public class ControllerResponseHandler implements ResponseBodyAdvice<Object> {
  
 private Logger logger = LogManager.getLogger(getClass());

 @Override
 public boolean supports(MethodParameter returnType, Class<? extends HttpMessageConverter<?>> converterType) {
  // 支持所有的返回值类型
  return true;
 }

 @Override
 public Object beforeBodyWrite(Object body, MethodParameter returnType, MediaType selectedContentType,
   Class<? extends HttpMessageConverter<?>> selectedConverterType, ServerHttpRequest request,
   ServerHttpResponse response) {
  if(body instanceof ResponseBean) {
   return body;
  } else {
   // 所有没有返回　ResponseBean　结构的结果均认为是成功的
   return ResponseBean.success(body);
  }
 }
}
```
