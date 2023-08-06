#!/usr/bin/env python
# coding: utf-8

# # $n$ queens job shop scheduling
# Adapted from https://github.com/timnon/pyschedule/blob/master/examples/n-queens-job-shop.py

# In[1]:


import processscheduler as ps

# In[2]:


# set input size to 5 just for readability, increasing up to 30 is ok
# to get a solution in a reasonable time
n = 36
pb = ps.SchedulingProblem('n_queens_type_scheduling', horizon=n)


# In[3]:


# resources
R = {i : ps.Worker('W-%i'%i) for i in range(n)}


# In[4]:


# tasks
T = {(i,j) : ps.FixedDurationTask('T-%i-%i'%(i,j), duration=1, optional=True) for i in range(n) for j in range(n)}


# In[5]:


# precedence constrains
for i in range(n):
    for j in range(1,n):
        c = ps.TaskPrecedence(T[i,j-1], T[i,j], offset=0)
        pb.add_constraint(c)


# In[6]:


# resource assignment modulo n
for j in range(n):
    for i in range(n):
        T[(i+j) % n,j].add_required_resource(R[i])


# In[7]:


# solve
solver = ps.SchedulingSolver(pb, verbosity=False, parallel=True)
sol = solver.solve()


# In[8]:


sol.render_gantt_matplotlib()

