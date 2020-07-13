[TOC]

# Spring boot 缓存

## 1. Spring boot 缓存用法

开门见山，直接介绍如何在Spring程序中使用缓存。

### 1.1 引入starter

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

### 1.2 在主类中开启缓存功能

```java
@SpringBootApplication
@EnableCaching //就是添加这个注释
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 1.3 在数据访问接口中添加注解

下面以JPA为例，如果使用Mybatis，则是在Mapper接口中添加：

```java
@CacheConfig(cacheNames = "users")
public interface UserRepository extends JpaRepository<User, Long> {

    @Cacheable
    User findByName(String name);

}
```

## 2. 相关注解说明

### 2.1 @CacheConfig

用于配置该类使用的缓存配置信息。@CachePut，@Cacheable，@CacheEvict的公共配置会放置到这个注解中。

包含的参数：

- cacheNames
缓存对象的名称，缓存存储的集合名称。如果我们对应Redis来思考，就能明白这个字段的含义。

- keyGenerator
指定默认的KeyGenerator的bean name。若需要指定一个自定义的key生成器，我们需要去实现org.springframework.cache.interceptor.KeyGenerator接口，并使用该参数来指定。需要注意的是：该参数与key是互斥的。

- cacheManager
用于指定使用哪个缓存管理器，非必需。只有当有多个时才需要使用。这里填写要用的那个管理器的bean name。

- cacheResolver
用于指定使用那个缓存解析器，非必需。需通过org.springframework.cache.interceptor.CacheResolver接口来实现自己的缓存解析器，并用该参数指定。

### 2.2 @Cacheable

除了有和@CacheConfig一样的参数之外，还有如下额外的参数：

- value
同cacheNames，在Spring 4中新增，是cacheNames的别名。

- key
缓存对象存储在Map集合中的key值，非必需，缺省按照函数的所有参数组合作为key值，若自己配置需使用SpEL表达式，比如：@Cacheable(key = "#p0")：使用函数第一个参数作为缓存的key值，更多关于SpEL表达式的详细内容可参考官方文档。

- condition
缓存对象的条件，非必需，也需使用SpEL表达式，只有满足表达式条件的内容才会被缓存，比如：@Cacheable(key = "#p0", condition = "#p0.length() < 3")，表示只有当第一个参数的长度小于3的时候才会被缓存，若做此配置上面的AAA用户就不会被缓存，读者可自行实验尝试。

- unless
另外一个缓存条件参数，非必需，需使用SpEL表达式。它不同于condition参数的地方在于它的判断时机，该条件是在函数被调用之后才做判断的，所以它可以通过对result进行判断。如果指定的条件为true，则结果不会被缓存。

- sync
指定是否异步缓存，默认false。

### 2.3 @CachePut

配置于函数上，能够根据参数定义条件来进行缓存，它与@Cacheable不同的是，它每次都会真是调用函数，所以主要用于数据新增和修改操作上。它的参数与@Cacheable类似。

先执行方法，然后添加缓存。

### 2.4 @CacheEvict

配置于函数上，通常用在删除方法上，用来从缓存中移除相应数据，注解的默认执行顺序是先执行方法，然后再清除缓存。除了同@Cacheable一样的参数之外，它还有下面两个参数：

- allEntries
非必需，默认为false。当为true时，会移除所有数据

- beforeInvocation
非必需，默认为false，会在调用方法之后移除数据。当为true时，会在调用方法之前移除数据。

### 2.5 @Caching

如果需要处理复杂的规则，那么就需要使用@Caching注解。这个注解包含cacheable、put、evict三个属性，分别对应于@Cacheable、@CachePut、@CacheEvict三个注解。

### 2.6 三个注解的综合举例

```java
package com.gong.springbootcache.controller;

import com.gong.springbootcache.bean.Employee;
import com.gong.springbootcache.service.EmployeeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.Caching;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class EmployeeController {

    @Autowired
    EmployeeService employeeService;

    //value：指定缓存的名字，每个缓存组件有一个唯一的名字。缓存组件由CacheManager进行管理。
    //key：缓存数据时用到的key，默认使用方法参数的值，1-方法返回值 key =
    //#id也可这么表示：#root.args[0]（第一个参数）
    //keyGenerator：指定生成缓存的组件id，使用key或keyGenerator其中一个即可
    //cacheManager，cacheResolver：指定交由哪个缓存管理器，使用其中一个参数即可
    //condition：指定符合条件时才进行缓存
    //unless：当unless指定的条件为true，方法的返回值就不会被缓存
    //sync：是否使用异步模式
    //"#root.methodName+'[+#id+]'"
    @Cacheable(value = "emp")
    @ResponseBody
    @RequestMapping("/emp/{id}")
    public Employee getEmp(@PathVariable("id") Integer id){
        Employee emp = employeeService.getEmp(id);
        return emp;
    }

    @CachePut(value = "emp",key="#employee.id")
    @ResponseBody
    @GetMapping("/emp")
    public Employee updateEmp(Employee employee){
        Employee emp =  employeeService.updateEmp(employee);
        return emp;
    }

    @CacheEvict(value = "emp",key = "#id")
    @ResponseBody
    @GetMapping("/emp/del/{id}")
    public String deleteEmp(@PathVariable("id") Integer id){
        //employeeService.deleteEmp(id);
        return "删除成功";
    }

    @Caching(
            cacheable = {
                    @Cacheable(value = "emp",key = "#lastName")
            },
            put = {
                    @CachePut(value = "emp",key = "#result.id"),
                    @CachePut(value = "emp",key = "#result.email"),
            }
    )
    @ResponseBody
    @RequestMapping("/emp/lastName/{lastName}")
    public Employee getEmpByLastName(@PathVariable("lastName") String lastName){
        Employee employee = employeeService.getEmpByLastName(lastName);
        return employee;
    }
}
```
