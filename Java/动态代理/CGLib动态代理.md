[TOC]

# CGlib动态代理

CGLIB，Code Generation Library，是一个基于ASM（开源的Java字节编辑类库）的字节码生成库，它允许我们在运行时对字节码进行修改和动态生成。CGLIB通过**继承方式**实现代理，在子类中**采用方法拦截的技术拦截所有父类方法的调用**并顺势织入横切逻辑。

CGLib和JDK创建动态代理方式的区别：

- JDK动态代理是**基于接口的方式**，换句话来说就是**代理类和目标类都实现同一个接口**，那么代理类和目标类的方法名就一样了；

- CGLib动态代理是代理类去**继承目标类**，然后重写其中目标类的方法啊，这样也可以保证代理类拥有目标类的同名方法。

CGLIB是一个强大的高性能的代码生成库。作为JDK动态代理的互补，它对于那些没有实现接口的类提供了代理方案。在底层，它使用ASM字节码操纵框架。

本质上来说，CGLIB通过产生子类覆盖非final方法来进行代理。它比使用Java反射的JDK动态代理方法更快。CGLIB不能代理一个final类或者final方法。通常来说，你可以使用JDK动态代理方法来创建代理，对于没有接口的情况或者性能因素，CGLIB是一个很好的选择。

CGLIC和Java JDK如何选择：

1）如果目标对象实现了接口，默认情况下会采用JDK的动态代理实现AOP。

2）如果目标对象实现了接口，可以强制使用CGLIB实现AOP。

3）如果目标对象没有实现了接口，必须采用CGLIB库，Spring会自动在JDK动态代理和CGLIB之间转换。

## 1. 基本用法

我们先通过基本的用法来直观感受一下CGLIB。

1. pom.xml引入依赖

```xml
<dependencies>
    <dependency>
        <groupId>${project.groupId}</groupId>
        <artifactId>cglib</artifactId>
        <version>${project.version}</version>
    </dependency>
    <dependency>
        <groupId>org.ow2.asm</groupId>
        <artifactId>asm</artifactId>
        <version>${asm.version}</version>
    </dependency>
</dependencies>
```

2. Java代码

创建要代理的类：

```java
package com.wyq.day527;

public class Dog{

    final public void run(String name) {
        System.out.println("狗"+name+"----run");
    }

    public void eat() {
        System.out.println("狗----eat");
    }
}
```

创建拦截器：

```java
package com.wyq.day527;

import java.lang.reflect.Method;

import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

public class MyMethodInterceptor implements MethodInterceptor{

    @Override
    public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy) throws Throwable {
        System.out.println("这里是对目标类进行增强！！！");
        //注意这里的方法调用，不是用反射哦！！！
        Object object = proxy.invokeSuper(obj, args);
        return object;
    }  
}
```

测试类：

```java
package com.wyq.day527;

import net.sf.cglib.core.DebuggingClassWriter;
import net.sf.cglib.proxy.Enhancer;

public class CgLibProxy {
    public static void main(String[] args) {
        //在指定目录下生成动态代理类，我们可以反编译看一下里面到底是一些什么东西
        System.setProperty(DebuggingClassWriter.DEBUG_LOCATION_PROPERTY, "D:\\java\\java_workapace");

        //创建Enhancer对象，类似于JDK动态代理的Proxy类，下一步就是设置几个参数
        Enhancer enhancer = new Enhancer();
        //设置目标类的字节码文件
        enhancer.setSuperclass(Dog.class);
        //设置回调函数
        enhancer.setCallback(new MyMethodInterceptor());

        //这里的creat方法就是正式创建代理类
        Dog proxyDog = (Dog)enhancer.create();
        //调用代理类的eat方法
        proxyDog.eat();
    }
}
```

## 2. 原理分析

### 2.1 MethodInterceptor接口

```java
package net.sf.cglib.proxy;

/**
 * General-purpose {@link Enhancer} callback which provides for "around advice".
 * @author Juozas Baliuka <a href="mailto:baliuka@mwm.lt">baliuka@mwm.lt</a>
 * @version $Id: MethodInterceptor.java,v 1.8 2004/06/24 21:15:20 herbyderby Exp $
 */
public interface MethodInterceptor
extends Callback
{
    /**
     * All generated proxied methods call this method instead of the original method.
     * The original method may either be invoked by normal reflection using the Method object,
     * or by using the MethodProxy (faster).
     * @param obj "this", the enhanced object
     * @param method intercepted Method
     * @param args argument array; primitive types are wrapped
     * @param proxy used to invoke super (non-intercepted method); may be called
     * as many times as needed
     * @throws Throwable any exception may be thrown; if so, super method will not be invoked
     * @return any value compatible with the signature of the proxied method. Method returning void will ignore this value.
     * @see MethodProxy
     */
    public Object intercept(Object obj, java.lang.reflect.Method method, Object[] args,
                               MethodProxy proxy) throws Throwable;

}
```

这个接口只有一个intercept()方法，这个方法有4个参数：

1）obj表示增强的对象，即实现这个接口类的一个对象；

2）method表示要被拦截的方法；

3）args表示要被拦截方法的参数；

4）proxy表示要触发父类的方法对象；

### 2.2 Enhancer

代理类的创建是通过Enhancer.create()方法创建代理对象，create()方法的源码：

```java

/**
     * Generate a new class if necessary and uses the specified
     * callbacks (if any) to create a new object instance.
     * Uses the no-arg constructor of the superclass.
     * @return a new instance
     */
    public Object create() {
        classOnly = false;
        argumentTypes = null;
        return createHelper();
    }
```

```java
private Object createHelper() {
        preValidate();
        Object key = KEY_FACTORY.newInstance((superclass != null) ? superclass.getName() : null,
                ReflectUtils.getNames(interfaces),
                filter == ALL_ZERO ? null : new WeakCacheKey<CallbackFilter>(filter),
                callbackTypes,
                useFactory,
                interceptDuringConstruction,
                serialVersionUID);
        this.currentKey = key;
        //调用父类方法创建代理类实例
        Object result = super.create(key);
        return result;
    }
```

父类create方法：

```java
protected Object create(Object key) {
        try {
            ClassLoader loader = getClassLoader();
            Map<ClassLoader, ClassLoaderData> cache = CACHE;
            ClassLoaderData data = cache.get(loader);
            if (data == null) {
                synchronized (AbstractClassGenerator.class) {
                    cache = CACHE;
                    data = cache.get(loader);
                    if (data == null) {
                        Map<ClassLoader, ClassLoaderData> newCache = new WeakHashMap<ClassLoader, ClassLoaderData>(cache);
                        data = new ClassLoaderData(loader);
                        newCache.put(loader, data);
                        CACHE = newCache;
                    }
                }
            }

            //先判断缓存是否存在
            this.key = key;
            Object obj = data.get(this, getUseCache());
            if (obj instanceof Class) {
                return firstInstance((Class) obj);
            }

            //创建实例的方法
            return nextInstance(obj);
        } catch (RuntimeException e) {
            throw e;
        } catch (Error e) {
            throw e;
        } catch (Exception e) {
            throw new CodeGenerationException(e);
        }
    }
```

nextInstance方法：

```java
protected Object nextInstance(Object instance) {
        EnhancerFactoryData data = (EnhancerFactoryData) instance;

        if (classOnly) {
            return data.generatedClass;
        }

        Class[] argumentTypes = this.argumentTypes;
        Object[] arguments = this.arguments;
        if (argumentTypes == null) {
            argumentTypes = Constants.EMPTY_CLASS_ARRAY;
            arguments = null;
        }
        return data.newInstance(argumentTypes, arguments, callbacks);
    }
```

```java
/**
         * Creates proxy instance for given argument types, and assigns the callbacks.
         * Ideally, for each proxy class, just one set of argument types should be used,
         * otherwise it would have to spend time on constructor lookup.
         * Technically, it is a re-implementation of {@link Enhancer#createUsingReflection(Class)},
         * with "cache {@link #setThreadCallbacks} and {@link #primaryConstructor}"
         *
         * @see #createUsingReflection(Class)
         * @param argumentTypes constructor argument types
         * @param arguments constructor arguments
         * @param callbacks callbacks to set for the new instance
         * @return newly created proxy
         */
        public Object newInstance(Class[] argumentTypes, Object[] arguments, Callback[] callbacks) {
            setThreadCallbacks(callbacks);
            try {
                // Explicit reference equality is added here just in case Arrays.equals does not have one
                if (primaryConstructorArgTypes == argumentTypes ||
                        Arrays.equals(primaryConstructorArgTypes, argumentTypes)) {
                    // If we have relevant Constructor instance at hand, just call it
                    // This skips "get constructors" machinery
                    return ReflectUtils.newInstance(primaryConstructor, arguments);
                }
                // Take a slow path if observing unexpected argument types
                return ReflectUtils.newInstance(generatedClass, argumentTypes, arguments);
            } finally {
                // clear thread callbacks to allow them to be gc'd
                setThreadCallbacks(null);
            }

        }
```

其中：

第一个参数为代理对象的构成器类型，第二个为代理对象构造方法参数，第三个为对应回调对象。

## 3. FastClass

Cglib中提供FastClass增强功能，FastClass顾名思义是一个能让被增强类更快调用的Class，主要针对调用方法是变量的场景，用于替代反射调用。

FastClass不使用反射类（Constructor或Method）来调用委托类方法，而是动态生成一个新的类（继承FastClass），向类中写入委托类实例直接调用方法的语句，用模板方式解决Java语法不支持问题，同时改善Java反射性能。（我的理解就是通过改善方法查找逻辑提高性能）

动态类为委托类方法调用语句建立索引，使用者根据方法签名（方法名+参数类型）得到索引值，再通过索引值进入相应的方法调用语句，得到调用结果。

```java
public abstract class FastClass{

    // 委托类
    private Class type;

    // 子类访问构造方法
    protected FastClass() {}
    protected FastClass(Class type) {
        this.type = type;
    }

    // 创建动态FastClass子类
    public static FastClass create(Class type) {
        // Generator：子类生成器，继承AbstractClassGenerator
        Generator gen = new Generator();
        gen.setType(type);
        gen.setClassLoader(type.getClassLoader());
        return gen.create();
    }

    /**
     * 调用委托类方法
     *
     * @param name 方法名
     * @param parameterTypes 方法参数类型
     * @param obj 委托类实例
     * @param args 方法参数对象
     */
    public Object invoke(String name, Class[] parameterTypes, Object obj, Object[] args) {
        return invoke(getIndex(name, parameterTypes), obj, args);
    }

    /**
     * 根据方法描述符找到方法索引
     *
     * @param name 方法名
     * @param parameterTypes 方法参数类型
     */
    public abstract int getIndex(String name, Class[] parameterTypes);

    /**
     * 根据方法索引调用委托类方法
     *
     * @param index 方法索引
     * @param obj 委托类实例
     * @param args 方法参数对象
     */
    public abstract Object invoke(int index, Object obj, Object[] args);

    /**
     * 调用委托类构造方法
     * 
     * @param parameterTypes 构造方法参数类型
     * @param args 构造方法参数对象
     */
    public Object newInstance(Class[] parameterTypes, Object[] args) throws {
        return newInstance(getIndex(parameterTypes), args);
    }

    /**
     * 根据构造方法描述符（参数类型）找到构造方法索引
     *
     * @param parameterTypes 构造方法参数类型
     */
    public abstract int getIndex(Class[] parameterTypes);

    /**
     * 根据构造方法索引调用委托类构造方法
     *
     * @param index 构造方法索引
     * @param args 构造方法参数对象
     */
    public abstract Object newInstance(int index, Object[] args);

}
```

### 3.1 例子

**委托类：**

```java
public class DelegateClass {

    public DelegateClass() {
    }

    public DelegateClass(String string) {
    }

    public boolean add(String string, int i) {
        System.out.println("This is add method: " + string + ", " + i);
        return true;
    }

    public void update() {
        System.out.println("This is update method");
    }
}
```

测试代码：

```java
public static void main(String[] args) throws Exception {
    // 保留生成的FastClass类文件
    System.setProperty(DebuggingClassWriter.DEBUG_LOCATION_PROPERTY, "D:\\Temp\\CGLib\\FastClass");

    Class delegateClass = DelegateClass.class;

    // Java Reflect

    // 反射构造类
    Constructor delegateConstructor = delegateClass.getConstructor(String.class);
    // 创建委托类实例
    DelegateClass delegateInstance = (DelegateClass) delegateConstructor.newInstance("Tom");

    // 反射方法类
    Method addMethod = delegateClass.getMethod("add", String.class, int.class);
    // 调用方法
    addMethod.invoke(delegateInstance, "Tom", 30);

    Method updateMethod = delegateClass.getMethod("update");
    updateMethod.invoke(delegateInstance);

    // CGLib FastClass

    // FastClass动态子类实例
    FastClass fastClass = FastClass.create(DelegateClass.class);

    // 创建委托类实例
    DelegateClass fastInstance = (DelegateClass) fastClass.newInstance(
        new Class[] {String.class}, new Object[]{"Jack"});

    // 调用委托类方法
    fastClass.invoke("add", new Class[]{ String.class, int.class}, fastInstance, new Object[]{ "Jack", 25});

    fastClass.invoke("update", new Class[]{}, fastInstance, new Object[]{});
}
```

### 3.2 底层分析

fastClass创建动态FastClass子类：

```java
public class DelegateClass$$FastClassByCGLIB$$4af5b667 extends FastClass {

    /**
     * 动态子类构造方法
     */
    public DelegateClass$$FastClassByCGLIB$$4af5b667(Class delegateClass) {
        super(delegateClass);
    }

    /**
     * 根据方法签名得到方法索引
     *
     * @param name 方法名
     * @param parameterTypes 方法参数类型
     */
    public int getIndex(String methodName, Class[] parameterTypes) {
        switch(methodName.hashCode()) {

            // 委托类方法add索引：0
            case 96417:
                if (methodName.equals("add")) {
                    switch(parameterTypes.length) {
                        case 2:
                            if (parameterTypes[0].getName().equals("java.lang.String") && 
                                parameterTypes[1].getName().equals("int")) {
                                return 0;
                            }
                    }
                }
                break;

            // 委托类方法update索引：1
            case -838846263:
                if (methodName.equals("update")) {
                    switch(parameterTypes.length) {
                        case 0:
                            return 1;
                    }
                }
                break;

            // Object方法equals索引：2
            case -1295482945:
                if (methodName.equals("equals")) {
                    switch(parameterTypes.length) {
                        case 1:
                            if (parameterTypes[0].getName().equals("java.lang.Object")) {
                                return 2;
                            }
                    }
                }
                break;

            // Object方法toString索引：3
            case -1776922004:
                if (methodName.equals("toString")) {
                    switch(parameterTypes.length) {
                        case 0: return 3;
                    }
                }
                break;

            // Object方法hashCode索引：4
            case 147696667:
                if (methodName.equals("hashCode")) {
                    switch(parameterTypes.length) {
                        case 0:
                            return 4;
                    }
                }
        }

        return -1;
    }

    /**
     * 根据方法索引调用委托类方法
     *
     * @param methodIndex 方法索引
     * @param delegateInstance 委托类实例
     * @param parameterValues 方法参数对象
     */
    public Object invoke(int methodIndex, Object delegateInstance, Object[] parameterValues) {
        DelegateClass instance = (DelegateClass) delegateInstance;
        int index = methodIndex;
        try {
            switch(index) {
                case 0:
                    // 委托类实例直接调用方法语句
                    return new Boolean(instance.add((String)parameterValues[0], 
                            ((Number)parameterValues[1]).intValue()));
                case 1:
                    instance.update();
                    return null;
                case 2:
                    return new Boolean(instance.equals(parameterValues[0]));
                case 3:
                    return instance.toString();
                case 4:
                    return new Integer(instance.hashCode());
            }
        } catch (Throwable t) {
            throw new InvocationTargetException(t);
        }

        throw new IllegalArgumentException("Cannot find matching method/constructor");
    }

    /**
     * 根据构造方法描述符（参数类型）找到构造方法索引
     *
     * @param parameterTypes 构造方法参数类型
     */
    public int getIndex(Class[] parameterTypes) {
        switch(parameterTypes.length) {
            // 无参构造方法索引：0
            case 0:
                return 0;

            // 有参构造方法索引：1
            case 1:
                if (parameterTypes[0].getName().equals("java.lang.String")) {
                    return 1;
                }
            default:
                return -1;
        }
    }

    /**
     * 根据构造方法索引调用委托类构造方法
     *
     * @param methodIndex 构造方法索引
     * @param parameterValues 构造方法参数对象
     */
    public Object newInstance(int methodIndex, Object[] parameterValues) {
        // 创建委托类实例
        DelegateClass newInstance = new DelegateClass;
        DelegateClass newObject = newInstance;
        int index = methodIndex;
        try {
            switch(index) {
                // 调用构造方法（<init>）
                case 0:
                    newObject.<init>();
                    return newInstance;
                case 1:
                    newObject.<init>((String)parameterValues[0]);
                    return newInstance;
            }
        } catch (Throwable t) {
            throw new InvocationTargetException(t);
        }

        throw new IllegalArgumentException("Cannot find matching method/constructor");
    }

    public int getMaxIndex() {
        return 4;
    }
}
```

## 参考

1. [CGLib动态代理](https://www.cnblogs.com/wyq1995/p/10945034.html)
2. [CGLib FastClass](https://www.jianshu.com/p/0604d79435f1)
