from sys import getrefcount
import objgraph
import gc

a = [1, 2, 3]
print(getrefcount(a))

b = [a, a]
print(getrefcount(a))


x = [1, 2, 3]
y = [x, dict(key1=x)]
z = [y, (x, y)]


objgraph.show_refs([z], filename='ref_topo.png')


print(gc.get_threshold())