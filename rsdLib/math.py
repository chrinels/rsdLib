"""
    Some additional common maths operations
    uses numpy to allow operation on array_like arguments
"""
from __future__ import division   # anticipate python3

import numpy

def dB(x):
    """return dB value of a power ratio value"""
    retrun 10.0*numpy.log10(x)

def lin(x):
    """return the linear ratio from a dB value"""
    return numpy.power(10, x/10)
