### 如何把同步的代码改成异步的

[董伟名博客](https://mp.weixin.qq.com/s?__biz=MzA3NDk1NjI0OQ==&mid=2247483864&idx=1&sn=9ce1061040a4ada28c1518b76e74ad54&chksm=9f76ad6ea8012478349e0a6b6b05080cbdd811943f859edc29c721d97221e502a5c7fed604d6&scene=21#wechat_redirect)

```
def handle(id):
    subject = get_subject_from_db(id)
    buyinfo = get_buyinfo(id)
    change = process(subject, buyinfo)
    notify_change(change)
    flush_cache(id)
```

可以看到，需要获取subject和buyinfo之后才能执行process，然后才能执行notify_change和flush_cache。

如果使用asyncio，就是这样写：

```
import asyncio
async def handle(id):
    subject = asyncio.ensure_future(get_subject_from_db(id))
    buyinfo = asyncio.ensure_future(get_buyinfo(id))
    results = await asyncio.gather(subject, buyinfo)
    change = await process(results)
    await notify_change(change)
    loop.call_soon(flush_cache, id)
```
原则上无非是让能一起协同的函数异步化（subject和buyinfo已经是Future对象了），然后通过gather获取到这些函数执行的结果；有顺序的就用call_soon来保证。

继续深入，现在详细了解下一步还有什么其他解决方案以及其应用场景：

包装成Future对象。上面使用了ensure_future来做，上篇也说过，也可以用loop.create_task。如果你看的是老文章可能会出现asyncio.async这种用法，它现在已经被弃用了。如果你已经非常熟悉，你也可以直接使用asyncio.Task(get_subject_from_db(id))这样的方式。

回调。上面用到了call_soon这种回调。除此之外还有如下两种：

loop.call_later(delay, func, *args)。延迟delay秒之后再执行。
loop.call_at(when, func, *args)。 某个时刻才执行。
其实套路就是这些罢了。