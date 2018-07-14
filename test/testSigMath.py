
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


from os import path
# show what is being tested and from where - pick one depending on need
print('\nTesting sig_math in package:\n',path.abspath(xxx.__package__))

if __name__=='__main__':
    unittest.main()
    
