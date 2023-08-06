import processscheduler as ps
import random

from z3 import *
import time
#set_option("parallel.enable", True)  # enable parallel computation
#set_option("parallel.threads.max", 16)  #nbr of max tasks
s = Optimize()

nb = 20000

for i in range(nb):
    x = Int('x_%i' % i)
    y = Int('y_%i' % i)
    b = Bool('b_%i' % i)
    s1 = And([x==i, y==-i, b==True])
    s2 = And([x==-i, y==i, b==False])
    s.add_soft(s1, 10)
    s.add_soft(s2, 10)
    s.add(Xor(s1, s2))
st = time.time()
s.check()
s.model()
fin = time.time()
print(fin-st)
print(s.statistics())

# second check
s2 = Solver()#For('QF_LIA')
for i in range(nb):
    x = Int('x_%i' % i)
    y = Int('y_%i' % i)
    b = Bool('b_%i' % i)
    s1b = And([x==i, y==-i, b==True])
    s2b = And([x==-i, y==i, b==False])
    s2.add(If(b, s1b, s2b))
st = time.time()
s2.check()
s2.model()
fin = time.time()
print(fin-st)
print(s2.statistics())    
