[TOC]

# Spring Boot单元测试

## Spring Boot 2.1.x之后使用JUnit5进行单元测试方式

在不同的Spring Boot版本中@ExtendWith的使用也有所不同，其中在Spring boot 2.1.x之前， @SpringBootTest 需要配合@ExtendWith(SpringExtension.class)才能正常工作的。

而在Spring boot 2.1.x之后，我们查看@SpringBootTest 的代码会发现，其中已经组合了@ExtendWith(SpringExtension.class)，因此，无需在进行该注解的使用了。

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@BootstrapWith(SpringBootTestContextBootstrapper.class)
@ExtendWith(SpringExtension.class)
public @interface SpringBootTest {
   @AliasFor("properties")
   String[] value() default {};
   @AliasFor("value")
   String[] properties() default {};
   Class<?>[] classes() default {};
   WebEnvironment webEnvironment() default WebEnvironment.MOCK;
   enum WebEnvironment {
      MOCK(false),
      RANDOM_PORT(true),
      DEFINED_PORT(true),
      NONE(false);
      …
   }
}
```

官方说明：

If you are using JUnit 4, don’t forget to also add @RunWith(SpringRunner.class) to your test, otherwise the annotations will be ignored. If you are using JUnit 5, there’s no need to add the equivalent @ExtendWith(SpringExtension.class) as @SpringBootTest and the other @…Test annotations are already annotated with it.

所以只需如下方式即可：

```java
@SpringBootTest
public class OrderServiceTest {
   @Resource
   private OrderService orderService;
   @Test
   public void testInsert() {
      Order order = new Order();
      order.setOrderNo("A001");
      order.setUserId(100);
      orderService.insert(order);
   }
}
```


