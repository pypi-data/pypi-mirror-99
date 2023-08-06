from xevo.eobj import eobj

import random

class phobia(eobj):
  pmute=0.3
  """implementing an phobic evolutionary object, requires an eobjplus"""
  def __init__(s,q=None,phob=None):
    s.initial()
    s.q=q
    if phob is None:phob=[]
    s.p=phob
  def __str__(s):
    return str(s.q)
  def __add__(a,b):
    return phobia(a.q+b.q,random.choice([a.p,b.p]))
  def shallmaximize(s):s.q.shallmaximize()

  
  def randomize(s):
    return phobia(s.q.randomize(),[])
  
  def alterpm(s):
    le=len(s.q.func)
    i=random.random()*le/1.0001
    if i in s.p:
      s.p.remove(i)
    else:
      s.p.append(i)
    while len(s.p)>=le:
      s.p=s.p[1:]
  def mutate(s):
    if random.random()<s.pmute:
      s.alterpm()
    # print("gonna mutate",s.q.func)
    return phobia(s.q._mutbyfunc([q for i,q in enumerate(s.q.func) if not i in s.p]),[i for i in s.p])
    
    
  def calcstrength(s):
    return s.q.calcstrength()
  def _copy(s):
    return phobia(s.q.copy(),[i for i in s.p])


