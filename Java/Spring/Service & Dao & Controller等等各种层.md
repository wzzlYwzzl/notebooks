[TOC]

# Spring代码中的各种“层”

在使用Spring或者Spring Boot框架编码时，我们时常会遇到各种“**层”的说法，比如：View层、Controller层、Service层、Dao层、Model层、Mapper层、Entity层等。

这里虽然说的是Spring，其实Java代码中都有这些层的身影，只是体现形式不一样了。

## 1. “层”的一点思考

说到分层，首先想到的就是MVC设计模式，它将这个模块分为三部分组成：Model、Controller、View，这三部分对应于三层，View层与Controller层交互，Controller层与Model层交互。这种设计模式提供了一种很好的模块设计思路。

我们使用SSM框架时，MVC设计模式的分层有了一定的变化，或者说有了更为细化的分层。

**View $\rightarrow$ controller $\rightarrow$ service  $\xrightarrow{Model/Entity}$ dao/mapper**

从上面的结构可以看出，MVC中的Model层变成了：service $\xrightarrow{Model/Entity}$ dao/mapper。

## 2. 不同层的说明

### 2.1 Service层

Service层叫服务层，被称为服务，粗略的理解就是对一个或多个DAO进行的再次封装，封装成一个服务，所以这里也就不会是一个原子操作了，需要事物控制。

在service层写业务逻辑代码的时候要注意，将每一个独立的功能写成一个单独的方法，方便其他的代码进行调用。

service层主要负责业务模块的应用逻辑应用设计。同样是首先设计接口，再设计其实现类，接着再Spring的配置文件中配置其实现的关联。这样我们就可以在应用中调用service接口来进行业务处理。service层的业务实，具体要调用已经定义的dao层接口，封装service层业务逻辑有利于通用的业务逻辑的独立性和重复利用性。程序显得非常简洁。

一个service应当只调用自己对应的dao，如果需要调用其他实体的操作，需要将其他实体的service引入来使用。

```java
@Service
public class UserAction {
     public List<User> getUserList(){
         List<User> userList= new ArrayList<>();
         userList.add(new User("11","男"));
         userList.add(new User("22","男"));
         userList.add(new User("33","男"));
         return userList;
     }
}
```

### 2.2 Model/Entity层

model层即数据库实体层，也被称为entity层，pojo层。一般数据库一张表对应一个实体类，类属性同表字段一一对应。

Model为view服务的，传递和接收view的数据。model与数据库表的字段映射，并且也添加前端需要的字段。毕竟model是为view服务的。而为了简洁就没有重复使用entity与数据库表一一对应。

模型层（model）一般是实体对象（把现实的的事物变成java中的对象），作用是一暂时存储数据方便持久化（存入数据库或者写入文件）作为一个包裹封装一些数据来在不同的层以及各种java对象中使用。

```java
package com.example.homework.model;

import org.springframework.stereotype.Repository;

@Repository
public class User {
    private Long id;
    private String username;
    private String Password;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }
}
```

### 2.3 Dao层/Mapper层/Repository层

Dao层是更为统一的表述，Mapper层是Spring Boot + mybatis框架中才有的，Repository层是标准Spring Data中引入的概念。

DAO层叫数据访问层，全称为data access object，属于一种比较底层，比较基础的操作，具体到对于某个表的增删改查，也就是说某个DAO一定是和数据库的某一张表一一对应的，其中封装了增删改查基本操作，建议DAO只做原子操作，增删改查。

```java
@Mapper
@Repository
public interface UserMapper {
    //注册成功，插入一条数据
    @Insert("insert into user(username,password) values (#{username},#{password})")
    void add(User user);
    //检验注册的username是否已经存在数据库中，通过User类创建findByUsername对象，传进username进行与数据库比较
    @Select("select * from user where username = #{username}")
    User findByUsername(@Param("username") String username);
    //登录用：检验账号密码是否正确
    @Select("select * from user where username = #{username} and password = #{password}")
    User findByUsername_login(@Param("username") String username,
                              @Param("password") String password);
}
```

### 2.4 Controller层

负责请求转发，接受页面过来的参数，传给Service层处理，接收反馈信息，再传给页面。

做一些service前后的数据处理，利用service完成更高的操作。作为View和Model中间层。

controller层只是负责从service层获得数据，发送到相应的视图，核心业务逻辑在service层。

```java
@Controller
public class LoginController {
    //实现自动装配
    @Autowired
    private UserMapper userMapper;

    //验证账号密码
    @PostMapping("/login")
    //获取三个参数，账号，密码，按钮是否被点击
    public String login(@Param("username") String username,
                        @Param("password") String password,
                        @Param("btn_login") String btn_login,
                        Model model) {
        User user = new User();
        user.setUsername(username);
        user.setPassword(password);
        //使用findByUsername_login（）方法，对数据库进行检查，判断账号密码是否正确
        User check_login = userMapper.findByUsername_login(username,password);
        //正确，返回index页面，错误，返回error页面
        if(check_login != null){
            int ok = 1;
            model.addAttribute("ok",ok);
            model.addAttribute("success_login_username",username);
            return "index";
        }else{
            model.addAttribute("error_btn_login",btn_login);
            model.addAttribute("error_login_username",username);
            model.addAttribute("error_login_password",password);
            return "error";
        }
    }
}  
```
