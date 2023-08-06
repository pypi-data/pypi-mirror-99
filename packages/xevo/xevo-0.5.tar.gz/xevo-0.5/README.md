# xevo
This is a simple set of classes to use for evolutionary coding in a polymorphic way. The central classes are given by "eobj", which implements the basic structure for an object that will be optimized by the second one "evo", which handles the optimization.

#eobj
Each eobj needs to at least implement:
def __add__(a,b):
  how to combine objects a and b
def randomize(s):
  return a new completely random version of this class
def mutate(s):
  return a sligthly mutated version of this object
def calcstrength(s)->float:
  how strong is this objects version
def _copy(s):
  copy the specifics of this object

you can also override shallmaximize->bool to chance if the strength should be maximized

Finally __init__(s) should not contain any nonoptional parameters and call s.initial()

There are two simple examples of this object. pion.py tries to find a fixed value (aka np.pi) and bitflip.py tries to maximize the sum of a list of booleans. This is very simple and implements a simple counter, that counts how often any state is evaluated. You can also take a look at the deep learning example below.

#evo
This object only needs to implement two functions
def generation(s)->None:
  update the objects (stored in s.q)
def _copy(s) -> "subclass of evo":
  copy the specifics of this object

Here there is a simple example implemented in crossevo (which is also given in the package), of a batch of object, in which 2 random objects figth against each other and the weaker one is replaced by either a combination of both objects, or by a mutation of the winning one.

#erun
Runs an experiment given an evo object and an eobj object. You can also specify the size population in the initializer.
To run the experiment call run(s,maxsteps=1000000,goalstrength=1000000.0), where maxsteps is the maximum number of generation calls that can be called. And by beating goalstrength the run is stopped before.
After the run, you can call show_history(s,log=False) to show a strength history (with an optional logarithmic y axis (if log=True))

#machine learning
If you take a look at the eobj deep (deep.py and deeptools.py), you find a simple optimizer object, which tries to find the perfect network setup for a keras dense network setup. So using it requires keras and tensorflow.







