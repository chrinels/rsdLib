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

def __startStop(n, start, stop, span):
    """start:stop or centre:span index range for an n sample sequence"""
    # n==0 for 0:len(samples) range 
    n_start = start if n==0 else int(round(start*n))
    n_stop = stop if n==0 else int(round(stop*n))
    if span:
        h_span = n_stop//2
        n_stop = n_start + h_span
        n_start -= h_span
    if n==0:
        # linear time sequence
        return n_start, n_stop
    else:
        # offset to line up with freqshift
        return n_start + n//2, n_stop + n//2

def timeSlice(samples, start, stop, span=False):
    """return (t, samples[t]) values of a slice of the signal in time,
       using either start, stop or centre, span"""
    xx = range(__startStop(0, start, stop, span))
    return xx, numpy.take(samples, xx)

def freqSlice(samples, start, stop, span=True):
    """return (f, X[f]) values of a slice of the FFT of the signal in 
       normalise freq, using either start, stop or centre, span"""
    n_samp = len(samples)
    n_start, n_stop = __startStop(n_samp, start, stop, span)
    # do FFT and shift
    fr = fftshift(fftfreq(n_samp))
    X = fftshift(fft(samples))
    # slice the result
    return fr[n_start:n_stop], numpy.take(X, range(n_start, n_stop))

def spectSlice(samples, start, stop, span=True, n_fft=512):
    """return (f, |X[f]|) values of a slice of the spectogram of the signal in
       normalise freq, using either start, stop or centre, span"""
    n_start, n_stop = __startStop(n_fft, start, stop, span)
    # do Spectogram using Welch's method - for now just use the default window
    X, fr = welch(samples, nfft=n_fft)
    # re-order, do shift and slice
    fr = fftshift(fr)
    X = fftshift(X)
    return fr[n_start:n_stop], numpy.take(X, range(n_start, n_stop))
