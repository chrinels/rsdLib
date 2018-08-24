"""
    Some additional common maths operations
    uses numpy to allow operation on array_like arguments
                                                      rgr12jan18
 * Copyright (C) 2018 Radio System Design Ltd.
 * Author: Richard G. Ranson, richard@radiosystemdesign.com
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation under
 * version 2.1 of the License.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
"""
from __future__ import division   # anticipate python3

import numpy as np
from numpy.fft import fft, fftfreq

from scipy.signal import welch

def dB(x, power=True):
    """return dB value of a power (false = voltage) ratio value"""
    _db = np.log10(x)
    if power:
        return 10.0*_db
    else:
        return 20.0*_db

def lin(x, power=True):
    """return the linear ratio from a dB power (false = voltage) value"""
    if power:
        _x = 0.1*np.array(x)
    else:
        _x = 0.05*np.array(x)
    return np.power(10, _x)

def fitCycles(cycles, length, complex=False):
    """time sequence with an exact number of cycles in the length given"""
    xx = np.arange(length)
    si = np.sin(2*np.pi*xx*cycles/length)
    if complex:
        return  np.cos(2*np.pi*xx*cycles/length) + 1j*si
    else:
        return si

def _fromSS(start, stop, dx=1):
    start = int(round(start)) if dx==1 else int(round(start*dx))
    stop = int(round(stop)) if dx==1 else int(round(stop*dx))
    return range(start, stop)

def _fromSC(centre, span, dx=1):
    h_span = int(span)//2 if dx==1 else int(round(span*dx))//2
    centre = int(centre) if dx==1 else int(round(centre*dx))
    return range(centre-h_span, centre+h_span)

def timeSlice(samples, start, stop, dt=1, span=False):
    """return (t, samples[t]) values of a slice of the signal in time,
       using either start, stop or if span=True centre, span"""
    if span:
        xx_range = _fromSC(start, stop, dx=1)
    else:
        xx_range = _fromSS(start, stop, dx=1)
    return xx_range, samples.take(xx_range, mode='wrap')

def freqIndex(a, fr):
    """"return the index of a that is closest to the frequency given"""
    # not certain about the dx variables here - all tests assume normalised fr
    return np.argmin(np.abs(a-fr*len(a)))

def freqSlice(samples, start, stop, df=1, span=True):
    """return (f, X[f]) values of a slice of the FFT of the signal in normalise
       freq, using either start, stop or if span=True centre, span"""
    n_samples = len(samples)
    if span:
        xx_range = _fromSC(start, stop, dx=1.0*n_samples)
    else:
        xx_range = _fromSS(start, stop, dx=1.0*n_samples)
    # do FFT and shift
    fr = fftfreq(n_samples)
    X = fft(samples)
    # slice the result
    return fr.take(xx_range, mode='wrap'), X.take(xx_range, mode='wrap')

def spectSlice(samples, start, stop, span=True, n_fft=256):
    """return (f, |X[f]|) values of a slice of the spectogram of the signal in
       normalise freq, using either start, stop or if span=True centre, span"""
    n_samples = len(samples)
    if span:
        xx_range = _fromSC(start, stop, dx=1.0*n_fft)
    else:
        xx_range = _fromSS(start, stop, dx=1.0*n_fft)
    # do Spectogram using Welch's method - for now just use the default window
    fr, X = welch(samples, nfft=n_fft)
    return fr.take(xx_range, mode='wrap'), X.take(xx_range, mode='wrap')

def timePower(samples):
    """return average power in the time samples given"""
    return np.mean(np.abs(samples)**2)

def freqPower(spectrum):
    """return average power in the spectrum given"""
    return timePower(spectrum)/len(spectrum)

if __name__=='__main__':
    import matplotlib.pylab as plt
    sx=fitCycles(64,1024, True)
    fr, X = freqSlice(sx, 0, 1)
