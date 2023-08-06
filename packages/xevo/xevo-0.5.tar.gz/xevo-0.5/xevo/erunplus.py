import matplotlib.pyplot as plt
import numpy as np
import time


from xevo.erun import erun

class erunplus(erun):
    
    def __init__(s,vo,obj,population=10,show=True,delay=None,custom_cancel=None):
        if custom_cancel is None:custom_cancel=lambda **kwargs:False
        s.custom_cancel=custom_cancel
        erun.__init__(s,vo,obj,population=population,show=show,delay=delay)
    
    def run(s,maxsteps=1000000,goalstrength=1000000.0):
        for i in range(maxsteps):
            mx,mm,ss=s.vo.logeneration(s.show)
            s.maxs.append(mx)
            s.means.append(mm)
            s.stds.append(ss)
            if s.custom_cancel(mx=mx,mm=mm,ss=ss,s=s):return
            if s.shallmaximize:
                if mx>=goalstrength:return
            else:
                if mx<=goalstrength:return
            if not s.delay is None:
                time.sleep(s.delay)
    
            








