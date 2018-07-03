import asyncio

class Task(asyncio.futures.Future):

    def __init__(self, gen, *,loop):
        super().__init__(loop=loop)
        self._gen = gen
        self._loop.call_soon(self._step)

    def _step(self, val=None, exc=None):
        """
        _step方法没有让协程执行完成，就会添加回调
        """
        try:
            if exc:
                f = self._gen.throw(exc)
            else:
                f = self._gen.send(val)
        except StopIteration as e:
            self.set_result(e.value)
        except Exception as e:
            self.set_exception(e)
        else:
            f.add_done_callback(
                 self._wakeup)

    def _wakeup(self, fut):
        """
        _wakeup又会继续执行_step... 直到协程程序完成，并set_result
        """
        try:
            res = fut.result()
        except Exception as e:
            self._step(None, e)
        else:
            self._step(res, None)

async def foo():
    await asyncio.sleep(2)
    print('Hello Foo')

async def bar():
    await asyncio.sleep(1)
    print('Hello Bar')

loop = asyncio.get_event_loop()
tasks = [Task(foo(), loop=loop),
         loop.create_task(bar())]
loop.run_until_complete(
        asyncio.wait(tasks))
loop.close()