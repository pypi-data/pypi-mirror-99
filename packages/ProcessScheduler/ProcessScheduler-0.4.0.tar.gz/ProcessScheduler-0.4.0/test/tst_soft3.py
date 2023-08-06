import processscheduler as ps
import random

from z3 import *
import time
set_option("parallel.enable", True)  # enable parallel computation
set_option("parallel.threads.max", 16)  #nbr of max tasks
s = Optimize()

nb = 10000

bools_vars_1 = []
for i in range(nb):
    x = Int('x_%i' % i)
    y = Int('y_%i' % i)
    b = Bool('b_%i' % i)
    bools_vars_1.append(b)
    s1 = And([x + y== 3 * i, x == i, b==True])
    s2 = And([x + y== 4 * i, x == 2 * i, b==False])
    s.add_soft(s1, 10)
    s.add_soft(s2, 10)
    s.add(Xor(s1, s2))
asst = PbEq([(applied, True) for applied in bools_vars_1], 50)
s.add(asst)
st = time.time()
s.check()
s.model()
fin = time.time()
print(fin-st)
print(s.statistics())

# second check
s2 = Solver()#For('QF_LIA')
bools_vars_2 = []
for i in range(nb):
    x = Int('x_%i' % i)
    y = Int('y_%i' % i)
    b = Bool('b_%i' % i)
    bools_vars_2.append(b)
    s1b = And([x + y== 3 * i, x == i, b==True])
    s2b = And([x + y== 4 * i, x == 2 * i, b==False])
    s2.add(If(b, s1b, s2b))
asst = PbEq([(applied, True) for applied in bools_vars_2], 50)
s2.add(asst)
st = time.time()
print(s2.check())
s2.model()
fin = time.time()
print(fin-st)
print(s2.statistics())    
