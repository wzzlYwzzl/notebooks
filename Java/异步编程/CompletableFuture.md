[TOC]

# CompletableFuture

CompletableFuture 是 Java 8 引入的新特性，用于异步编程。

## 1. Future vs CompletableFuture

CompletableFuture 是 Future API 的扩展。

Future 被用于作为一个异步计算结果的引用。提供一个 isDone() 方法来检查计算任务是否完成。当任务完成时，get() 方法用来接收计算任务的结果。

Future API 是非常好的 Java 异步编程进阶，但是它缺乏一些非常重要和有用的特性。

1. 不能手动完成
   当你写了一个函数，用于通过一个远程 API 获取一个电子商务产品最新价格。因为这个 API 太耗时，你把它允许在一个独立的线程中，并且从你的函数中返回一个 Future。现在假设这个 API 服务宕机了，这时你想通过该产品的最新缓存价格手工完成这个 Future 。你会发现无法这样做。

2. Future 的结果在非阻塞的情况下，不能执行更进一步的操作
   Future 不会通知你它已经完成了，它提供了一个阻塞的 get() 方法通知你结果。你无法给 Future 植入一个回调函数，当 Future 结果可用的时候，用该回调函数自动的调用 Future 的结果。

3. 多个 Future 不能串联在一起组成链式调用
   有时候你需要执行一个长时间运行的计算任务，并且当计算任务完成的时候，你需要把它的计算结果发送给另外一个长时间运行的计算任务等等。你会发现你无法使用 Future 创建这样的一个工作流。

4. 不能组合多个 Future 的结果
   假设你有 10 个不同的 Future，你想并行的运行，然后在它们运行未完成后运行一些函数。你会发现你也无法使用 Future 这样做。

5. 没有异常处理
   Future API 没有任务的异常处理结构居然有如此多的限制，幸好我们有 CompletableFuture，你可以使用 CompletableFuture 达到以上所有目的。

`CompletableFuture` 实现了 `Future` 和 `CompletionStage` 接口，并且提供了许多关于创建，链式调用和组合多个 `Future` 的便利方法集，而且有广泛的异常处理支持。

## 2. CompletableFuture 使用

### 2.1 简单的例子

可以使用如下无参构造函数简单的创建 CompletableFuture

```java
CompletableFuture<String> completableFuture = new CompletableFuture<String>();
```

这是一个最简单的 `CompletableFuture`，想获取 `CompletableFuture` 的结果可以使用 `CompletableFuture.get()` 方法：

```java
String result = completableFuture.get()
```

`get()` 方法会一直阻塞直到 Future 完成。因此，以上的调用将被永远阻塞，因为该 Future 一直不会完成。

你可以使用 `CompletableFuture.complete()` 手工的完成一个 Future：

```java
completableFuture.complete("Future's Result")
```

所有等待这个 Future 的客户端都将得到一个指定的结果，并且 `completableFuture.complete()` 之后的调用将被忽略。

### 2.2 使用 runAsync() 运行异步计算

运行异步计算 如果你想异步的运行一个后台任务并且不想改任务返回任务东西，这时候可以使用 `CompletableFuture.runAsync()` 方法，它持有一个 `Runnable` 对象，并返回 `CompletableFuture<Void>` 。

```java
// Run a task specified by a Runnable Object asynchronously.
CompletableFuture<Void> future = CompletableFuture.runAsync(new Runnable() {
    @Override
    public void run() {
        // Simulate a long-running Job
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            throw new IllegalStateException(e);
        }
        System.out.println("I'll run in a separate thread than the main thread.");
    }
});

// Block and wait for the future to complete
future.get()
```

你也可以以 lambda 表达式的形式传入 Runnable 对象：

```java
// Using Lambda Expression
CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
    // Simulate a long-running Job
    try {
        TimeUnit.SECONDS.sleep(1);
    } catch (InterruptedException e) {
        throw new IllegalStateException(e);
    }
    System.out.println("I'll run in a separate thread than the main thread.");
});
```

### 2.3 使用 `supplyAsync()` 运行一个异步任务并且返回结果

当任务不需要返回任何东西的时候， `CompletableFuture.runAsync()` 非常有用。但是如果你的后台任务需要返回一些结果应该要怎么样？
`CompletableFuture.supplyAsync()` 就是你的选择。它持有`supplier<T>` 并且返回 `CompletableFuture<T>`，T 是通过调用 传入的 supplier 取得的值的类型。

```java
// Run a task specified by a Supplier object asynchronously
CompletableFuture<String> future = CompletableFuture.supplyAsync(new Supplier<String>() {
    @Override
    public String get() {
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            throw new IllegalStateException(e);
        }
        return "Result of the asynchronous computation";
    }
});

// Block and get the result of the Future
String result = future.get();
System.out.println(result);
```

`Supplier<T>` 是一个简单的函数式接口，表示 supplier 的结果。它有一个 get()方法，该方法可以写入你的后台任务中，并且返回结果。

**关于 Executor 和 Thread Pool 笔记**

你可能想知道，我们知道 runAsync()和 supplyAsync()方法在单独的线程中执行他们的任务。但是我们不会永远只创建一个线程。
CompletableFuture 可以从全局的 ForkJoinPool.commonPool()获得一个线程中执行这些任务。
但是你也可以创建一个线程池并传给 runAsync()和 supplyAsync()方法来让他们从线程池中获取一个线程执行它们的任务。
CompletableFuture API 的所有方法都有两个变体-一个接受 Executor 作为参数，另一个不这样：

```java
// Variations of runAsync() and supplyAsync() methods
static CompletableFuture<Void>  runAsync(Runnable runnable)
static CompletableFuture<Void>  runAsync(Runnable runnable, Executor executor)
static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier)
static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier, Executor executor)
```

创建一个线程池，并传递给其中一个方法：

```java
Executor executor = Executors.newFixedThreadPool(10);
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    try {
        TimeUnit.SECONDS.sleep(1);
    } catch (InterruptedException e) {
        throw new IllegalStateException(e);
    }
    return "Result of the asynchronous computation";
}, executor);
```

## 3. 在 CompletableFuture 传入回调方法

`CompletableFuture.get()` 方法是阻塞的。它会一直等到 Future 完成并且在完成后返回结果。
但是，这是我们想要的吗？对于构建异步系统，我们应该附上一个回调给`CompletableFuture`，当 Future 完成的时候，自动的获取结果。
如果我们不想等待结果返回，我们可以把需要等待 Future 完成执行的逻辑写入到回调函数中。

可以使用 `thenApply()`, `thenAccept()` 和 `thenRun()`方法附上一个回调给 CompletableFuture。

### 3.1 thenApply()

可以使用 `thenApply()` 处理和改变 `CompletableFuture` 的结果。持有一个 `Function<R,T>`作为参数。`Function<R,T>`是一个简单的函数式接口，接受一个 T 类型的参数，产出一个 R 类型的结果。

```java
// Create a CompletableFuture
CompletableFuture<String> whatsYourNameFuture = CompletableFuture.supplyAsync(() -> {
   try {
       TimeUnit.SECONDS.sleep(1);
   } catch (InterruptedException e) {
       throw new IllegalStateException(e);
   }
   return "Rajeev";
});

// Attach a callback to the Future using thenApply()
CompletableFuture<String> greetingFuture = whatsYourNameFuture.thenApply(name -> {
   return "Hello " + name;
});

// Block and get the result of the future.
System.out.println(greetingFuture.get()); // Hello Rajeev
```

你也可以通过附加一系列的 `thenApply()`在回调方法 在 `CompletableFuture` 写一个连续的转换。这样的话，结果中的一个 `thenApply` 方法就会传递给该系列的另外一个 `thenApply` 方法。

```java
CompletableFuture<String> welcomeText = CompletableFuture.supplyAsync(() -> {
    try {
        TimeUnit.SECONDS.sleep(1);
    } catch (InterruptedException e) {
       throw new IllegalStateException(e);
    }
    return "Rajeev";
}).thenApply(name -> {
    return "Hello " + name;
}).thenApply(greeting -> {
    return greeting + ", Welcome to the CalliCoder Blog";
});

System.out.println(welcomeText.get());
// Prints - Hello Rajeev, Welcome to the CalliCoder Blog
```

### 3.2 thenAccept() 和 thenRun()

如果你不想从你的回调函数中返回任何东西，仅仅想在 Future 完成后运行一些代码片段，你可以使用 `thenAccept()`和 `thenRun()`方法，这些方法经常在调用链的最末端的最后一个回调函数中使用。
`CompletableFuture.thenAccept()`持有一个 `Consumer<T>`，返回一个 `CompletableFuture<Void>`。它可以访问 `CompletableFuture` 的结果：

```java
// thenAccept() example
CompletableFuture.supplyAsync(() -> {
    return ProductService.getProductDetail(productId);
}).thenAccept(product -> {
    System.out.println("Got product detail from remote service " + product.getName())
});
```

虽然 `thenAccept()`可以访问 `CompletableFuture` 的结果，但 `thenRun()`不能访 `Future` 的结果，它持有一个 `Runnable` 返回 `CompletableFuture`：

```java
// thenRun() example
CompletableFuture.supplyAsync(() -> {
    // Run some computation
}).thenRun(() -> {
    // Computation Finished.
});
```

**异步回调方法的笔记**

CompletableFuture 提供的所有回调方法都有两个变体：

```java
// thenApply() variants
<U> CompletableFuture<U> thenApply(Function<? super T,? extends U> fn);
<U> CompletableFuture<U> thenApplyAsync(Function<? super T,? extends U> fn);
<U> CompletableFuture<U> thenApplyAsync(Function<? super T,? extends U> fn, Executor executor);
```

这些异步回调变体通过在独立的线程中执行回调任务帮助你进一步执行并行计算。
以下示例：

```java
CompletableFuture.supplyAsync(() -> {
    try {
       TimeUnit.SECONDS.sleep(1);
    } catch (InterruptedException e) {
      throw new IllegalStateException(e);
    }
    return "Some Result"
}).thenApply(result -> {
    /*
      Executed in the same thread where the supplyAsync() task is executed
      or in the main thread If the supplyAsync() task completes immediately (Remove sleep() call to verify)
    */
    return "Processed Result"
})
```

在以上示例中，在 `thenApply()`中的任务和在 `supplyAsync()`中的任务执行在相同的线程中。任何 `supplyAsync()`立即执行完成,那就是执行在主线程中（尝试删除 sleep 测试下）。
为了控制执行回调任务的线程，你可以使用异步回调。如果你使用 `thenApplyAsync()`回调，将从 `ForkJoinPool.commonPool()`获取不同的线程执行。

```java
CompletableFuture.supplyAsync(() -> {
    return "Some Result"
}).thenApplyAsync(result -> {
    // Executed in a different thread from ForkJoinPool.commonPool()
    return "Processed Result"
})
```

此外，如果你传入一个 Executor 到 thenApplyAsync()回调中，，任务将从 Executor 线程池获取一个线程执行。

```java
Executor executor = Executors.newFixedThreadPool(2);
CompletableFuture.supplyAsync(() -> {
    return "Some result"
}).thenApplyAsync(result -> {
    // Executed in a thread obtained from the executor
    return "Processed Result"
}, executor);
```

## 4. 组合多个 CompletableFuture

### 4.1 组合两个 CompletableFuture

1. **使用 thenCompose()组合两个独立的 future**

假设你想从一个远程 API 中获取一个用户的详细信息，一旦用户信息可用，你想从另外一个服务中获取他的贷方。 考虑下以下两个方法 `getUserDetail()`和 `getCreditRating()`的实现：

```java
CompletableFuture<User> getUsersDetail(String userId) {
    return CompletableFuture.supplyAsync(() -> {
    UserService.getUserDetails(userId);
    });
}

CompletableFuture<Double> getCreditRating(User user) {
    return CompletableFuture.supplyAsync(() -> {
    CreditRatingService.getCreditRating(user);
    });
}
```

```java
CompletableFuture<Double> result = getUserDetail(userId)
.thenCompose(user -> getCreditRating(user));
```

如果你的回调函数返回一个 CompletableFuture，但是你想从 CompletableFuture 链中获取一个直接合并后的结果，这时候你可以使用 `thenCompose()`。

2. **使用 thenCombine()组合两个独立的 future**

虽然 thenCompose()被用于当一个 future 依赖另外一个 future 的时候用来组合两个 future。thenCombine()被用来当两个独立的 Future 都完成的时候，用来做一些事情。

```java
System.out.println("Retrieving weight.");
CompletableFuture<Double> weightInKgFuture = CompletableFuture.supplyAsync(() -> {
    try {
        TimeUnit.SECONDS.sleep(1);
    } catch (InterruptedException e) {
       throw new IllegalStateException(e);
    }
    return 65.0;
});

System.out.println("Retrieving height.");
CompletableFuture<Double> heightInCmFuture = CompletableFuture.supplyAsync(() -> {
    try {
        TimeUnit.SECONDS.sleep(1);
    } catch (InterruptedException e) {
       throw new IllegalStateException(e);
    }
    return 177.8;
});

System.out.println("Calculating BMI.");
CompletableFuture<Double> combinedFuture = weightInKgFuture
        .thenCombine(heightInCmFuture, (weightInKg, heightInCm) -> {
    Double heightInMeter = heightInCm/100;
    return weightInKg/(heightInMeter*heightInMeter);
});

System.out.println("Your BMI is - " + combinedFuture.get());
```

当两个 Future 都完成的时候，传给``thenCombine()的回调函数将被调用。

### 4.2 组合多个 CompletableFuture

我们使用 `thenCompose()`和 `thenCombine()`把两个 CompletableFuture 组合在一起。现在如果你想组合任意数量的 `CompletableFuture`，应该怎么做？我们可以使用以下两个方法组合任意数量的 `CompletableFuture`。

```java
static CompletableFuture<Void> allOf(CompletableFuture<?>... cfs)
static CompletableFuture<Object> anyOf(CompletableFuture<?>... cfs)
```

1. **CompletableFuture.allOf()**

`CompletableFuture.allOf` 的使用场景是当你一个列表的独立 future，并且你想在它们都完成后并行的做一些事情。

假设你想下载一个网站的 100 个不同的页面。你可以串行的做这个操作，但是这非常消耗时间。因此你想写一个函数，传入一个页面链接，返回一个 CompletableFuture，异步的下载页面内容。

```java
CompletableFuture<String> downloadWebPage(String pageLink) {
    return CompletableFuture.supplyAsync(() -> {
    // Code to download and return the web page's content
    });
}
```

现在，当所有的页面已经下载完毕，你想计算包含关键字 CompletableFuture 页面的数量。可以使用 CompletableFuture.allOf()达成目的。

```java
List<String> webPageLinks = Arrays.asList(...) // A list of 100 web page links

// Download contents of all the web pages asynchronously
List<CompletableFuture<String>> pageContentFutures = webPageLinks.stream()
        .map(webPageLink -> downloadWebPage(webPageLink))
        .collect(Collectors.toList());


// Create a combined Future using allOf()
CompletableFuture<Void> allFutures = CompletableFuture.allOf(
        pageContentFutures.toArray(new CompletableFuture[pageContentFutures.size()])
);
```

使用 CompletableFuture.allOf()的问题是它返回 CompletableFuture。但是我们可以通过写一些额外的代码来获取所有封装的 CompletableFuture 结果。

```java
// When all the Futures are completed, call `future.join()` to get their results and collect the results in a list -
CompletableFuture<List<String>> allPageContentsFuture = allFutures.thenApply(v -> {
   return pageContentFutures.stream()
           .map(pageContentFuture -> pageContentFuture.join())
           .collect(Collectors.toList());
});

```

当所有 future 完成的时候，我们调用了 future.join()，因此我们不会在任何地方阻塞。join()方法和 get()方法非常类似，这唯一不同的地方是如果最顶层的 CompletableFuture 完成的时候发生了异常，它会抛出一个未经检查的异常。

2. **CompletableFuture.anyOf()**

CompletableFuture.anyOf()和其名字介绍的一样，当任何一个 CompletableFuture 完成的时候【相同的结果类型】，返回一个新的 CompletableFuture。以下示例：

```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> {
    try {
        TimeUnit.SECONDS.sleep(2);
    } catch (InterruptedException e) {
       throw new IllegalStateException(e);
    }
    return "Result of Future 1";
});

CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> {
    try {
        TimeUnit.SECONDS.sleep(1);
    } catch (InterruptedException e) {
       throw new IllegalStateException(e);
    }
    return "Result of Future 2";
});

CompletableFuture<String> future3 = CompletableFuture.supplyAsync(() -> {
    try {
        TimeUnit.SECONDS.sleep(3);
    } catch (InterruptedException e) {
       throw new IllegalStateException(e);
    }
    return "Result of Future 3";
});

CompletableFuture<Object> anyOfFuture = CompletableFuture.anyOf(future1, future2, future3);

System.out.println(anyOfFuture.get()); // Result of Future 2
```

在以上示例中，当三个中的任何一个 CompletableFuture 完成， anyOfFuture 就会完成。因为 future2 的休眠时间最少，因此她最先完成，最终的结果将是 future2 的结果。

`CompletableFuture.anyOf()`传入一个 Future 可变参数，返回 CompletableFuture。`CompletableFuture.anyOf()`的问题是如果你的 CompletableFuture 返回的结果是不同类型的，这时候你讲会不知道你最终 CompletableFuture 是什么类型。

## 5. CompletableFuture 异常处理

首先让我们明白在一个回调链中错误是怎么传递的。思考下以下回调链：

```java
CompletableFuture.supplyAsync(() -> {
    // Code which might throw an exception
    return "Some result";
}).thenApply(result -> {
    return "processed result";
}).thenApply(result -> {
    return "result after further processing";
}).thenAccept(result -> {
    // do something with the final result
});
```

如果在原始的 supplyAsync()任务中发生一个错误，这时候没有任何 thenApply 会被调用并且 future 将以一个异常结束。如果在第一个 thenApply 发生错误，这时候第二个和第三个将不会被调用，同样的，future 将以异常结束。

### 5.1 使用 exceptionally() 回调处理异常

exceptionally()回调给你一个从原始 Future 中生成的错误恢复的机会。你可以在这里记录这个异常并返回一个默认值。

```java
Integer age = -1;

CompletableFuture<String> maturityFuture = CompletableFuture.supplyAsync(() -> {
    if(age < 0) {
        throw new IllegalArgumentException("Age can not be negative");
    }
    if(age > 18) {
        return "Adult";
    } else {
        return "Child";
    }
}).exceptionally(ex -> {
    System.out.println("Oops! We have an exception - " + ex.getMessage());
    return "Unknown!";
});

System.out.println("Maturity : " + maturityFuture.get()); 
```

### 5.2 使用 handle() 方法处理异常

API提供了一个更通用的方法 - handle()从异常恢复，无论一个异常是否发生它都会被调用。

```java
Integer age = -1;

CompletableFuture<String> maturityFuture = CompletableFuture.supplyAsync(() -> {
    if(age < 0) {
        throw new IllegalArgumentException("Age can not be negative");
    }
    if(age > 18) {
        return "Adult";
    } else {
        return "Child";
    }
}).handle((res, ex) -> {
    if(ex != null) {
        System.out.println("Oops! We have an exception - " + ex.getMessage());
        return "Unknown!";
    }
    return res;
});

System.out.println("Maturity : " + maturityFuture.get());
```

如果异常发生，res参数将是 null，否则，ex将是 null。
