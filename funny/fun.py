# import string
# mydict = {x[0]:x[1] for x in zip(string.ascii_letters,range(1,27))}
# def chaword(str):
#     return sum([mydict[x.lower()] for x in str])
#
# print(chaword("unscrupulously"))

flag = {'i': 0}
def func(b,e):
    flag['i'] += 1
    index = flag['i']
    m = int((b+e) / 2)
    print(">>>", b, e, m, "index:", index)
    if (b != m):
        func(b, m)
        func(m, e)
        print("!!!", m,e, "index:", index)

import asyncio

@asyncio.coroutine
def func():
    for i in range(10):
        print("a_%s" %i)
        yield from asyncio.sleep(0.5)
    return

def func2():
    for i in range(10):
        print("b_%s" %i)
        yield from asyncio.sleep(0.5)
    return

def func3():
    a = yield from asyncio.async(func())
    b = yield from asyncio.async(func2())
    print(a)
    print(b)

# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(func3())
# loop.close()()

class A():
    def __init__(self, a,b):
        self.a = 1
        self.b = 2

    def show(self):
        print(self.a)
        print(self.b)

class B(A):
    def show(self):
        print(self.a + 1)
        print(self.b + 1)

class C(B,A):
    pass
a = B(1,2)
c = C(1,2)
a.show()
print(c.__mro__)
