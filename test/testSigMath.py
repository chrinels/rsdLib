
"""
    Using unittest to validate code for sig_math in rsdLib module
                                                         rgr11july18
    look for #!# lines where corrections are pending
"""
from __future__ import print_function

import unittest
# for numpy operations, there are additional assertTests in the numpy module
import numpy.testing as npt
# npt.assert_almost_equal(actual, desired, decimal=7, err_msg='', verbose=True)

import rsdLib
from rsdLib import sig_math as xxx
import numpy as np

class TestSigMath(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # enables "test != result" in error message

    def tearDown(self):
        pass

    # everything starting test is run, but in no guaranteed order    
    def testdB(self):
        """check dB works for single or array like parameters"""
        npt.assert_almost_equal(xxx.dB(0.5), -3.0103, decimal=5,
                                err_msg="single value dB evaluation")
        npt.assert_almost_equal(xxx.dB((0.5, 1, 2)),
                                [-3.0103, 0, 3.0103], decimal=5,
                                err_msg="array value dB evaluation")
        # also for voltage option
        npt.assert_almost_equal(xxx.dB(0.5, False), -6.0206, decimal=5,
                                err_msg="single value dB evaluation")

    def testLin(self):
        """check lin works for single or array like parameters"""
        npt.assert_almost_equal(xxx.lin(-3), 0.50119, decimal=5,
                                err_msg="single value lin evaluation")
        npt.assert_almost_equal(xxx.lin((-3, 0, 3, 20)),
                                [0.50119, 1.00, 1.99526, 100.0], decimal=5,
                                err_msg="array value lin evaluation")
        # also for voltage option
        npt.assert_almost_equal(xxx.lin(-6, False), 0.50119, decimal=5,
                                err_msg="single value lin evaluation")

    def testFitCycles(self):
        """check the time sequence generated"""
        # real sequence
        s1 = xxx.fitCycles(100, 1024)
        self.assertFalse(np.iscomplexobj(s1), "waveform is not complex")
        self.assertEqual(s1[0], 0, "sin(0)=0")
        npt.assert_almost_equal(s1[1], -s1[-1], decimal=10,
                                err_msg="sin has odd symmetry")
        npt.assert_almost_equal(s1[512], 0, decimal=10,
                                err_msg="even number of cycles")
        # complex sequence
        s2 = xxx.fitCycles(99, 1024, complex=True)
        self.assertTrue(np.iscomplexobj(s2), "waveform is complex")
        self.assertEqual(s2.real[0], 1, "cos(0)=0")
        self.assertEqual(s2.imag[0], 0, "image is sin()")
        npt.assert_almost_equal(s2.real[1], s2.real[-1], decimal=10,
                                err_msg="cos has even symmetry")

    def testTimeSlice(self):
        """check slice of a time sequence"""
        s2 = xxx.fitCycles(64, 1024, True)  # exact sequence in the range
        x, y = xxx.timeSlice(s2, 100, 200)  # slice a start:stop section
        self.assertEqual(s2.real[100], y.real[0], "start in the right place")
        self.assertEqual(s2.real[199], y.real[-1], "end in the right place")
        x, y = xxx.timeSlice(s2, 400, 200, span=True)  # slice a  section
        self.assertEqual(s2.real[300], y.real[0], "start in the right place")        
        self.assertEqual(s2.real[499], y.real[-1], "end in the right place")
        # slice and wrap round the end
        x, y = xxx.timeSlice(s2, 1024, 200, span=True)
        self.assertEqual(x[0], 924, "x axis stays the same")
        self.assertEqual(s2.real[0], y.real[100], "y axis wraps end - beginning")
        
    def testFreqSlice(self):
        """check slice of a frequency sequence"""
        s1 = xxx.fitCycles(64, 1024)  # exact sequence in 1 FFT bin
        df = 1.0/1024
        neg_bin = 512 - 64
        pos_bin = 512 + 64
        x, Y = xxx.freqSlice(s1, 0, 1) # all the normalised range
        self.assertEqual(x[0], -0.5, "lower bound of freq range")
        self.assertEqual(x[-1], 0.5-df, "upper bound of freq range")
        # look for peak values
        npt.assert_almost_equal(Y[neg_bin], 0+512j, decimal=10,
                                err_msg="real time sin +j")
        npt.assert_almost_equal(Y[pos_bin], 0-512j, decimal=10,
                                err_msg="real time sin -j")
        #x, Y = xxx.freqSlice(s1, 1.0/neg_bin, 16*df) # 8 samples each side
        s2 = xxx.fitCycles(64, 1024, True)  # exact sequence in 1 FFT bin
        # complex so only 1 peak
        x2, Y2 = xxx.freqSlice(s2, 0, 1)
        npt.assert_almost_equal(Y2[neg_bin], 0, decimal=10,
                                err_msg="C+jS time -f=0")
        npt.assert_almost_equal(Y2[pos_bin], 1024, decimal=10,
                                err_msg="C+jS time +f=1")

    def testSpectSlice(self):
        """check slice of a spectrum sequence"""
        s1 = xxx.fitCycles(64, 1024, True)  # exact sequence in 1 FFT bin
        nfft = 256
        pos_bin = 256//2 + int(1024/64)
        fr, X = xxx.spectSlice(s1, 0, 1, n_fft=nfft)
        self.assertEqual(np.argmax(X), pos_bin, "correct spectrum max")
        
from os import path
# show what is being tested and from where - pick one depending on need
print('\nTesting sig_math in package:\n',path.abspath(xxx.__package__))

if __name__=='__main__':
    unittest.main()
    
