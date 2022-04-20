"""
Works for bivariate as well as multivariate constraints
"""

from CSP_Solver.Util import toRemove, MRV, LCV
from time import time

def BackTrack(obj, Mrv, start, timeout):
    if time() - start > timeout:
        return
    if Mrv.finished():
        obj.stop = 1
        return
    current = Mrv.minimum()
    cur = current[1]
    if len(obj.domains[cur]) == 0:
        return 
    Mrv.remove(current)
    Values = LCV(obj, cur)
    obj.givenValue[cur] = True
    for value in Values:
        Removed = toRemove(obj, cur, value[1])
        for rem in Removed:
            Mrv.decrease((len(obj.domains[rem[0]]),rem[0]))
            obj.domains[rem[0]].discard(rem[1])
        BackTrack(obj, Mrv, start, timeout)
        if obj.stop:
            return 
        for rem in Removed:
            Mrv.increase((len(obj.domains[rem[0]]),rem[0]))
            obj.domains[rem[0]].add(rem[1])
    Mrv.add(current)
    obj.givenValue[cur] = False

def ForwardChecking_MRV_LCV(obj, timeout):
    start = time()
    Mrv = MRV(obj)
    BackTrack(obj, Mrv, start, timeout)