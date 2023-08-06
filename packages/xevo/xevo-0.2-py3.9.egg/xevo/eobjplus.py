from xevo.eobj import eobj

import random
from abc import abstractmethod

class eobjplus(eobj):
  """eobj, but multiple functions"""
  def initial(s):
    eobj.initial(s)
    s.func=[]#list of dictionaries of type {"f":func()->eobjplus,"ws":probablility}
    s.regall()
  
  @abstractmethod
  def regall(s):
    """register all functions, needs to be overwritten"""
    pass
  
  def register(s,f,ws=1.0):
    s.func.append({"f":f,"ws":ws})
  
  def __init__(s,q=None):
    s.initial()
    s.q=q

  def _mutbyfunc(s,func):
    sm=0.0
    for fun in func:
      sm+=fun["ws"]
    r=random.random()*sm/1.00001
    for fun in func:
      if r<fun["ws"]:
        return fun["f"]()
      else:
        r-=fun["ws"]
    if len(fun)>0:
      return random.choice(fun)["f"]()
    else:
      return random.choice(s.func)["f"]()

  def mutate(s):
    return s._mutbyfunc(s.func)
  
  def copy(s):
    ret=s._copy()
    ret.regall()
    return ret


