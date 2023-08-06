from xevo.eobj import eobj

import numpy as np

class pion(eobj):
  """trivial test eobj trying to find the exact value of pi"""
  def __init__(s,q=3):
    s.initial()
    s.q=q
  def __str__(s):
    return str(s.q)
  def __add__(a,b):
    return pion((a.q+b.q)/2)
  def shallmaximize(s):return False

  
  def randomize(s):
    return pion(np.random.random()*2+2)
  def mutate(s):
    sn=s.q
    alpha=2*np.random.random()-1
    power=-10*np.random.random()
    sn+=alpha*np.exp(power)
    return pion(sn)
  def calcstrength(s):
    return np.abs(s.q-np.pi)
  def _copy(s):
    return pion(s.q)
