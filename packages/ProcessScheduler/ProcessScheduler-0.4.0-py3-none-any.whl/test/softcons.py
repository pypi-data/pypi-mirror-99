from z3 import *

x, y, z = Ints('x y z')

s = Optimize()
s.add(x > y)
s.add(y > z)
s.add(z > 0)
s.add_soft(x > y +1)
h = s.minimize(x)
print(s.check())
print(s.model())
print(h.value())

s = Optimize()
s.add(x > y)
s.add(y > z)
s.add(z > 0)
h = s.minimize(x)
s.add_soft(x > y +1)
print(s.check())
print(s.model())
print(h.value())
