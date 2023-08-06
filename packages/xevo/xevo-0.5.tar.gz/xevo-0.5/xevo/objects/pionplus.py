from xevo.eobjplus import eobjplus

import numpy as np

class pionplus(eobjplus):
  """trivial test eobj trying to find the exact value of pi"""
  def __init__(s,q=3):
    s.initial()
    s.q=q

  def __str__(s):
    return str(s.q)
  def __add__(a,b):
    return pionplus((a.q+b.q)/2)
  def shallmaximize(s):return False

  def regall(s):
    s.func=[]
    s.register(s.mutate1)
    s.register(s.mutate2)
    s.register(s.mutate3)
    s.register(s.mutate4)

  
  def randomize(s):
    return pionplus(np.random.random()*2+2)
  def mutate1(s):
    sn=s.q
    alpha=np.random.random()
    power=-10*np.random.random()
    sn+=alpha*np.exp(power)
    return pionplus(sn)
  def mutate2(s):
    sn=s.q
    alpha=-np.random.random()
    power=-10*np.random.random()
    sn+=alpha*np.exp(power)
    return pionplus(sn)
  def mutate3(s):
    sn=s.q
    alpha=2*np.random.random()-1
    power=-5-5*np.random.random()
    sn+=alpha*np.exp(power)
    return pionplus(sn)
  def mutate4(s):
    sn=s.q
    alpha=2*np.random.random()-1
    power=-5*np.random.random()
    sn+=alpha*np.exp(power)
    return pionplus(sn)
  
  def calcstrength(s):
    return np.abs(s.q-np.pi)
  def _copy(s):
    return pionplus(s.q)
