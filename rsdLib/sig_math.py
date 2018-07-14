"""
    Some additional common maths operations
    uses numpy to allow operation on array_like arguments
"""
from __future__ import division   # anticipate python3

import numpy

def dB(x, power=True):
    """return dB value of a power (false = voltage) ratio value"""
    _db = numpy.log10(x)
    if power:
        return 10.0*_db
    else:
        return 20.0*_db

def lin(x, power=True):
    """return the linear ratio from a dB power (false = voltage) value"""
    if power:
        _x = 0.1*numpy.array(x)
    else:
        _x = 0.05*numpy.array(x)
    return numpy.power(10, _x)
