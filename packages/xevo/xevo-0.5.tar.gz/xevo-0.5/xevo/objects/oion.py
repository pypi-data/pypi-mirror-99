from xevo.eobj import eobj
from xevo.oobj import oobj

import numpy as np

class oion(oobj):
    """modification of pion, to result in multiplicates of pi (for orthogonal optimisation)"""
    def __init__(s,q=3):
        s.initial()
        s.q=q
    def __str__(s):
        return str(s.q)
    def __add__(a,b):
        return oion((a.q+b.q)/2)
    def shallmaximize(s):return False

    
    def randomize(s):
        return oion(np.random.random()*100)
    def mutate(s):
        sn=s.q
        alpha=2*np.random.random()-1
        power=-10*np.random.random()+1#+1 compared to pion, since bigger range
        sn+=alpha*np.exp(power)
        return oion(sn)
    def calcstrength(s):
        return np.abs(np.sin(s.q))
    def _copy(s):
        return oion(s.q)
    def calcortho(s):
        return s.q
