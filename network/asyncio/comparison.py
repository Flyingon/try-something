import time
import requests
import asyncio
import aiohttp
import math
from concurrent.futures import ThreadPoolExecutor
NUMBERS = list(range(12))
URL = 'http://httpbin.org/get?a={}'

def fetch(a):
    r = requests.get(URL.format(a))
    return r.json()['args']['a']

start = time.time()
with ThreadPoolExecutor(max_workers=3) as executor:
    for num, result in zip(NUMBERS, executor.map(fetch, NUMBERS)):
        print(('fetch({}) = {}'.format(num, result)))
print(('Use requests+ThreadPoolExecutor cost: {}'.format(time.time() - start)))

async def run_scraper_tasks(executor):  # 当我们给一个函数添加了async关键字，就会把它变成一个异步函数
    loop = asyncio.get_event_loop()  # 每个线程有一个事件循环，主线程调用asyncio.get_event_loop时会创建事件循环，你需要把异步的任务丢给这个循环的run_until_complete方法，事件循环会安排协同程序的执行。和方法名字一样，异步的任务完成方法才会就执行完成了
    blocking_tasks = []
    for num in NUMBERS:
        task = loop.run_in_executor(executor, fetch, num)  # 为了在asyncio中使用concurrent.futures的执行器，我这用到了run_in_executor，它可以接收要同步执行的任务。
        task.__num = num   # 给task设置__num属性，是因为后面的completed中的Future对象只包含结果，但是我们并不知道num是什么，所以hack了下，之后的例子中会有其他的方案，本文是给大家提供各种解题的思路，在合适的场景还是有用处的
        blocking_tasks.append(task)
    completed, pending = await asyncio.wait(blocking_tasks)  # await asyncio.wait(blocking_tasks)就是协同的执行那些同步的任务，直到完成
    print(("-"*5, completed, pending ))
    results = {t.__num: t.result() for t in completed}  # 最后根据__num找到和执行结果的对应关系，排序然后打印结果。
    for num, result in sorted(list(results.items()), key=lambda x: x[0]):
        print(('fetch({}) = {}'.format(num, result)))
start = time.time()
executor = ThreadPoolExecutor(3)
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(
    run_scraper_tasks(executor)
)
print(('Use asyncio+requests+ThreadPoolExecutor cost: {}'.format(time.time() - start)))

async def fetch_async(a):
    async with aiohttp.request('GET', URL.format(a)) as r:
        data = await r.json()  # 希望能进行协程切换的地方，就需要使用await关键字。如上的例子中r.json方法会等待I/O（也就是正在做一个网络请求），这种就可以切换去做其他的时候，之后再切换回来。
    return data['args']['a']

start = time.time()
event_loop = asyncio.get_event_loop()
tasks = [fetch_async(num) for num in NUMBERS]
results = event_loop.run_until_complete(asyncio.gather(*tasks))  # asyncio.gather可以按顺序搜集异步任务执行的结果，我们就不需要用到之前提过的__num
for num, result in zip(NUMBERS, results):
    print(('fetch({}) = {}'.format(num, result)))
print(('Use asyncio+aiohttp cost: {}'.format(time.time() - start)))

async def fetch_async(a):
    async with aiohttp.request('GET', URL.format(a)) as r:
        data = await r.json()
    return a, data['args']['a']
def sub_loop(numbers):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [fetch_async(num) for num in numbers]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    for num, result in results:
        print(('fetch({}) = {}'.format(num, result)))
async def run(executor, numbers):
    await asyncio.get_event_loop().run_in_executor(executor, sub_loop, numbers)
def chunks(l, size):
    n = math.ceil(len(l) / size)
    for i in range(0, len(l), n):
        yield l[i:i + n]
event_loop = asyncio.get_event_loop()
tasks = [run(executor, chunked) for chunked in chunks(NUMBERS, 3)]
results = event_loop.run_until_complete(asyncio.gather(*tasks))
print(('Use asyncio+aiohttp+ThreadPoolExecutor cost: {}'.format(time.time() - start)))