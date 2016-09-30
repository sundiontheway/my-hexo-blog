title: 从python的协程理解tornado的异步处理
date: 2015-05-31
categories: Python

---

刚接触tornado时候最疑惑的问题就是tornado.gen.coroutine是怎么实现的。如何在代码中用同步格式实现异步效果。看了几次源码发现其实就是python协程的一个具体应用。下面从生成器开始，说说tornado的异步。

<!--more-->

### python协程

python利用yield关键字实现生成器，yield就像生化危机里的T病毒，被yield感染的函数都不仅仅是函数，而是一个函数生成器。函数生成器实例化后可以不断调用next方法吐出yield后的值。见下面代码：

```python

def gen():
    while True:
        a = yield
        print a

b = gen()
b.next() # 直接返回，无输出
b.send(16) # 打印16

```

如上面代码，函数gen()因为存在`yield`关键字，就变成了一个生成器函数，实例化这个生成器函数gen得到b，调用b的`next()`方法，会执行gen()，直到遇到第一个yield关键字后返回yield后的值（第一次执行直接返回，没有返回值），这时如果继续调用b.next(),就会每次读到yield处返回一个值。但是倘若调用b的send()方法，就会传递一个值到给生成器，CPU会从刚才挂起的状态开始继续，从yield后传入此值继续执行直到再遇到yield。

这其实就是用生成器来实现一个协程的例子，程序在需要跳转的地方被挂起，CPU跳转到其他代码执行，一旦需要继续刚才的状态，就用send发送一个值。但是这有什么用呢？没错，就是接下来要讲的异步IO。当执行到一段需要等待IO返回结果的代码时，为了提高效率，可以将当前执行状态挂起，转而去干其他事情。一旦IO处理完毕，就触发回调函数，回调函数里执行上述的send()方法，将处理结果传递回之前的状态里，程序再次回到之前挂起的状态，继续执行刚才未完成的操作。

### tornado的异步

tornado使用自己的异步装饰器gen.coroutine装饰需要异步操作的handler的get(或post)方法:

```python

@tornado.gen.coroutine
def get():
    result = yield foo()
    return result

```

下面看看这个装饰器做了哪些操作（不了解装饰器的朋友请自行搜索一下，这是python的最好用的语法糖）。我根据需要精简了部分代码，请自行查看源码了解更多：

```python
def _make_coroutine_wrapper(func, replace_callback):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = TracebackFuture()

        if replace_callback and 'callback' in kwargs:
            callback = kwargs.pop('callback')
            IOLoop.current().add_future(
                future, lambda future: callback(future.result()))

        try:
            result = func(*args, **kwargs)
        except (Return, StopIteration) as e:
            result = getattr(e, 'value', None)
        except Exception:
            future.set_exc_info(sys.exc_info())
            return future
        else:
            if isinstance(result, types.GeneratorType):
                try:
                    orig_stack_contexts = stack_context._state.contexts
                    yielded = next(result)
                    if stack_context._state.contexts is not orig_stack_contexts:
                        yielded = TracebackFuture()
                        yielded.set_exception(
                            stack_context.StackContextInconsistentError(
                                'stack_context inconsistency (probably caused '
                                'by yield within a "with StackContext" block)'))
                except (StopIteration, Return) as e:
                    future.set_result(getattr(e, 'value', None))
                except Exception:
                    future.set_exc_info(sys.exc_info())
                else:
                    Runner(result, future, yielded)
                try:
                    return future
                finally:
        future.set_result(result)
        return future
    return wrapper

```

分析一下，首先开头部分判断如果有callback函数，就把callback加入ioloop。否则把被修饰的func实例化为一个生成器result（即上面代码里的get()函数，因为yield的缘故，get已经成为一个生成器函数），然后执行一次next(result)，注意，在上上面的代码中，get()中yield的方法foo()是异步操作，所以通知IO后没有等待，直接return，就像最开始说的协程示例一样，修饰器里的next(result)也直接返回，异步操作被挂起，之后实例化一个Runner，Runner内部会将自己的callback放入ioloop，callback中包含了send方法。一旦IO处理完毕，ioloop就调用callback，callback再调用send将结果塞回yield之后的代码处，CPU跳回来继续执行之前挂起的函数。
整个过程下来，代码看起来是从头到尾行云流水，但是内部实现的逻辑却是利用python的协程，让CPU在不同的代码间自如跳转，为IO处理实现异步化。

