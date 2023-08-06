from xevo.evo import evo

import numpy as np
import time
import random

class trajmute(evo):
    def __init__(s):
        s.initial()



    def generation(s)->None:
        for i in range(len(s.q)):
            s.q[i]=s.q[i].mutate()
        stre=[zw.strength()* (1 if zw.shallmaximize() else -1)  for zw in s.q]
        wori=np.argmin(stre)
        s.q[wori]=np.random.choice(s.q,p=[float(wori!=i)/(len(s.q)-1) for i in range(len(s.q))])

    

    def _copy(s):
        return trajmute()



