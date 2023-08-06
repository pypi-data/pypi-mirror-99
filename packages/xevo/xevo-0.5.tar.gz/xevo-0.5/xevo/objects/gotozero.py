from xevo.eobj import eobj

import numpy as np
import time

class gotozero(eobj):
  """eobj that tries to move nd ints to zero"""
  def __init__(s,q=None):
    if q is None:q=[10,10]
    #print("initialising gotozero with")
    #print(q)
    #time.sleep(1)
    s.initial()
    s.q=q
  def __str__(s):
    return str(s.q)
  def __add__(a,b):
    return gotozero([aa+bb for aa,bb in zip(a,b)])
  def shallmaximize(s):return False

  
  def randomize(s):
    return s.copy()#that kind of a bodge i guess
    return gotozero([np.random.randint(-10,11) for i in range(len(s.q))])
  def mutate(s):
    s0=s
    s=s.copy()
    i=np.random.randint(len(s.q))
    s.q[i]+=np.random.choice([-1,1])
    return s
  def calcstrength(s):
    return np.sum([zw**2 for zw in s.q])
  def _copy(s):
    return gotozero(q=[zw for zw in s.q])
