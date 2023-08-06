from xevo.evo import evo

import numpy as np
import time
        

class orthoevo(evo):
    """similar to lineevo and crossevo but uses oobj to define neighbourhood as similarity. Can only work with 1d similarity and ignores everything else. Works, but the drawback is that this is a lot slower (ignoring the sort, this requires still 2x-4x epochs)"""
    
    def __init__(s,wsmerge=0.3,dex=0):
        s.initial()
        s.wsmerge=wsmerge
        s.dex=dex



    def generation(s)->None:
        s.q.sort(key=lambda x:x.ortho()[s.dex])
        i1=np.random.randint(len(s.q)-1)
        i2=i1+1
        i1won=s.q[i1].figth(s.q[i2])
        iwon=i1
        ilost=i2
        if not i1won:
            iwon=i2
            ilost=i1
        if np.random.random()<s.wsmerge:
            s.q[ilost]+=s.q[iwon]
        else:
            s.q[ilost]=s.q[iwon].mutate()
        
        


    def _copy(s):
        return orthoevo(s.wsmerge,s.dex)



