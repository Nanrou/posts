# asyncio翻译

## 摘要

这个模块提供基础接口来方便我们用协程方式写单线程的并发代码，可以用在基于socket和其他方式的复用IO，网络的客户端和服务端，和其他相关的基础构件。这里是一些需要注意的地方：

* 一个基于不同系统实现的可热插的事件循环
* 传输与协议的抽象化（类似于Twisted）
* 具体支持TCP，UDP，SSL，子进程管道，延迟调用和其他（其中有些是要依赖相关系统的）
* `Future`类是模仿了`concurrent.futures`类的，它被改成适用于事件循环
* 协程机制和任务（tasks）是基于`yield from`（译者注：现在是`await`啦），这个语法帮助我们在同步框架下写协程的代码
* `Future`类和协程都支持取消操作
* 在一个单独线程内的协程中的同步构件之间交互，是模仿了`threading`模块的
* 提供了一个将`work`转移到线程池的接口，你可以在确定要用这个库来生成阻塞IO操作的时候用

