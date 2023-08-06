from xevo.oobj import oobj

import random

class mob(oobj):
    """multiple oobj are also an oobj"""

    def __init__(s,gen_new=None,d=3,mutws=1.0,shallrnd=True):
        s.initial()
        s.d=d
        s.mutws=mutws

        if gen_new is None:return#allow initialisations without generation
        s.gen_new=gen_new

        s.q=[gen_new() for i in range(d)]

        s.odim=s.q[0].orthodim()*d

        if shallrnd:s.q=s.randomize().q


    def __str__(s):
        return "|".join([str(zw) for zw in s.q])

    def __add__(a,b):
        ret=a.copy()
        for i in range(ret.d):
            ret.q[i]+=b.q[i]
        return ret


    def shallmaximize(s):
        return s.q[0].shallmaximize()

    def randomize(s):
        ret=s.copy()
        for i in range(len(ret.q)):
            ret.q[i]=ret.q[i].randomize()
        return ret
    def mutate(s):
        ret=s.copy()
        for i in range(len(ret.q)):
            if random.random()>s.mutws:continue
            ret.q[i]=ret.q[i].mutate()
        return ret
    def calcstrength(s):
        p=1.0
        for zw in s.q:
            p*=zw.strength()
        return p**(1/s.d)
    def _copy(s):
        ret=mob()
        ret.gen_new=s.gen_new
        ret.d=s.d
        ret.q=[zw.copy() for zw in s.q]
        ret.odim=s.odim
        ret.mutws=s.mutws

        return ret

    def orthodim(s):
        return s.odim
    def calcortho(s):
        ret=[]
        #print("calc ortho")
        for zw in s.q:
            #print(zw)
            for zx in zw.ortho():
                ret.append(zx)
        return ret
   












