from xevo.evo import evo

import numpy as np
import time
import random

class trivmute(evo):
  """take x, if 50%->mutate (if better->set x, else ignore) else randomize"""
  
  def initial(s):
    s.q=None
    s.i=0
  def populate(s,person,n=10)->None:
    s.q=person.copy()#.randomize()
  
  def winner(s)->int:
    return 0
  def topn(s,n=3)->"[int]":
    return [0]
  def average(s)->"float,float":
    return s.q.strength(),0
  
  def __getitem__(s,key):
    return s.q
  def __set_item__(s,key,obj):
    s.q=obj
  
  def copy(s):
    ret=s._copy()
    if not s.q is None:ret.q=s.q.copy()
    return ret
  
  def __init__(s):
    s.initial()



  def generation(s)->None:
    os=s.q.strength()
    if random.random()<0.5:
      n=s.q.randomize()
    else:
      n=s.q.mutate()
    ns=n.strength()
    if ns<=os:
      s.q=n
      if hasattr(s.q,"getsave"):s.q.getsave()("data/bestobj.txt")
    
    


  def _copy(s):
    return trivmute()



