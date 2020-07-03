[TOC]

# Spring Boot中使用拦截器

基于Spring MVC的拦截器使用方式可能是借助于XML配置文件，但是这并不是很符合Spring Boot的使用思路，所以使用Spring Boot时，我们可以借助于程序完成拦截器的添加。

```java
@Configuration //只要能够被Spring扫描到即可
public class WebMvcConfigurer extends WebMvcConfigurerAdapter {

    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new HandlerInterceptorAdapter() {

            @Override
            public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
                                     Object handler) throws Exception {
                System.out.println("interceptor====222");
                return true;
            }
        }).addPathPatterns("/*");
    }
}
```
