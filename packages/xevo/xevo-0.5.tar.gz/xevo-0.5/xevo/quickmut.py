from xevo.crossevo import crossevo
from xevo.erun import erun

from xevo.erunplus import erunplus


def quickmut(obj,population=20,goal=0.0,maxsteps=1000,show=True,opt=None):

    if opt is None:opt=crossevo()

    c=erun(opt,obj,population=population,show=show)
    c.run(goalstrength=goal,maxsteps=maxsteps)
    return c.getwinner()


def semiquickmut(obj,population=20,goal=0.0,maxsteps=1000,show=True,opt=None):

    if opt is None:opt=crossevo()

    c=erun(opt,obj,population=population,show=show)
    c.run(goalstrength=goal,maxsteps=maxsteps)
    return c.vo.q



def meanquickmut(obj,population=20,goal_max=0.0,goal_mean=0.0,maxsteps=1000,show=True,opt=None):

    def cancel(s,mm,**kwargs):
        if s.shallmaximize:
            return mm>goal_mean
        else:
            return mm<goal_mean


    if opt is None:opt=crossevo()

    c=erunplus(opt,obj,population=population,show=show,custom_cancel=cancel)
    c.run(goalstrength=goal_max,maxsteps=maxsteps)
    return c.vo.q




