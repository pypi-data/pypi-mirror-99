from xevo.evo import evo

import numpy as np
import time
import random

class trajmuteplus(evo):
    def __init__(s):
        s.initial()



    def generation(s)->None:
        s.q=[zw.mutate() for zw in s.q]
        i1=np.random.randint(len(s.q))
        i2=i1
        #print(i1,i2,len(s.q))
        while i2==i1 and (not len(s.q)<2):
            i2=np.random.randint(len(s.q))
        s1=s.q[i1].strength()
        s2=s.q[i2].strength()
        if not s.q[i1].shallmaximize():s1*=-1
        if not s.q[i2].shallmaximize():s2*=-1
        if s1<s2:
            s.q[i1]=s.q[i2]
        else:
            s.q[i2]=s.q[i1]


    

    def _copy(s):
        return trajmuteplus()



