from xevo.evo import evo

import numpy as np
import time
        

class morthoevo(evo):
    """orthoevo, but using highdimensional definition of similarity. Does not neccesarily produce better results than orthoevo, since orthoevo seems to produce similar groups in higher dimensions (if d1 is 3 than d3=9)"""
    
    def __init__(s,wsmerge=0.3):
        s.initial()
        s.wsmerge=wsmerge



    def generation(s)->None:
        acd=np.random.randint(s.q[0].orthodim())
        s.q.sort(key=lambda x:x.ortho()[acd])
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
        ret= morthoevo(s.wsmerge)
        return ret


