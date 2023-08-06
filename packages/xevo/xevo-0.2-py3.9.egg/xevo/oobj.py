from xevo.eobj import eobj

from abc import abstractmethod,ABCMeta


class oobj(eobj):
    """equivalent zu eobj, but contains also functions to define similarity"""


    def ortho(s) -> "returns [dimensions], number defined in orthodim(s)":
        if (not hasattr(s,"oo")) or s.oo is None:
            s.oo=s.calcortho()
            if type(s.oo)!=list:
                s.oo=[s.oo]
        return s.oo

    @abstractmethod
    def calcortho(s):
        """calculate index values that define similarity"""
        pass

    def orthodim(s)->"dimensionality of the output":return 1

    def copy(s)->"subclass of oobj":
        ret=eobj.copy(s)
        #if hasattr(s,"oo"):
        #    ret.oo=s.oo
        return ret




