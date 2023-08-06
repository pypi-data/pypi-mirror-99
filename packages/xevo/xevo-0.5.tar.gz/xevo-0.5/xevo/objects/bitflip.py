from xevo.eobj import eobj

import numpy as np

class scounter:
  def __init__(s):
    s.i=0
  def pp(s):
    s.i+=1
  def __repr__(s):
    return str(s)
  def __str__(s):
    return str(s.i)
  def reset(s):
    s.i=0

counter=scounter()


class bitflip(eobj):
  """trivial test eobj trying to maximize the sum of a list of 100 booleans. Also counts each call to calcstrength"""
  def __init__(s,q=None):
    s.initial()
    s.q=q
    if q is None:s.q=s.randomize().q
  def __str__(s):
    return "".join([str(qq) for qq in s.q])
  def __add__(a,b):
    ret=[]
    for aa,bb in zip(a.q,b.q):
      if np.random.randint(2)==0:
        ret.append(aa)
      else:
        ret.append(bb)
    return bitflip(ret)
  
  def randomize(s):
    ret=[]
    for i in range(100):
      ret.append(np.random.randint(2))
    return bitflip(ret)
  def mutate(s):
    rel=[p for p in s.q]
    i=np.random.randint(len(rel))
    rel[i]=1-rel[i]
    return bitflip(rel)
  def calcstrength(s):
    counter.pp()
    return float(np.sum(s.q))
  def _copy(s):
    return bitflip([p for p in s.q])
