from xevo.eobj import eobj

from xevo.oobj import oobj


import numpy as np



class dualflip(oobj):
    """trivial test eobj trying to maximize the sum of a list of 100 booleans."""
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
        return dualflip(ret)
    
    def randomize(s):
        ret=[]
        for i in range(100):
            ret.append(np.random.randint(2))
        return dualflip(ret)
    def mutate(s):
        rel=[p for p in s.q]
        i=np.random.randint(len(rel))
        rel[i]=1-rel[i]
        return dualflip(rel)
    def calcstrength(s):
        return abs(2*(float(np.sum(s.q))-50))/100#lets define it on the more usual range
    def _copy(s):
        return dualflip([p for p in s.q])

    def calcortho(s):
        return float(np.mean(s.q))

    def orthodim(s):return 1






    

