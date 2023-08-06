from xevo.evo import evo

import numpy as np
import time
import random

from xevo.optimizers.trivmute import *


class trivmutetraj(trivmute):
    """trivmute, but for traj applications"""
    def __init__(s,forget=0):
        s.initial()
        s.forget=forget



    def generation(s)->None:
        os=s.q.strength()
        n=s.q.mutate()
        ns=n.strength()
        if (ns<=os) != n.shallmaximize():
            s.q=n
        else:s.forget+=1

    


    def _copy(s):
        return trivmutetraj(forget=s.forget)

    def __str__(s):
        return "trivmutetraj in "+str(s.forget)
    def __repr__(s):
        return str(s)


