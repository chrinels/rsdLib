
"""
    Using unittest to validate code for changeExt in fileUtils module
                                                         rgr11july18
    look for #!# lines where corrections are pending
"""
from __future__ import print_function

import unittest

SIMPLE_TEST_NAME = 'aName'
PATH_TEST_NAME = 'some/where/aName'

from rsdLib import fileUtils
from rsdLib.fileUtils import changeExt 
class TestSigMath(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # enables "test != result" in error message

    def tearDown(self):
        pass

    def testChangeExt(self):
        """check  fiel extension modifier works"""
        ans = changeExt(SIMPLE_TEST_NAME, '.bak')
        self.assertEqual(ans, SIMPLE_TEST_NAME+'.bak',
                         'add ext if none in the original')
        ans = changeExt(SIMPLE_TEST_NAME, 'bak')
        self.assertEqual(ans, SIMPLE_TEST_NAME+'.bak',
                         'add .ext if the . is omitted')
        ans = changeExt(PATH_TEST_NAME, '.bak')
        self.assertEqual(ans, PATH_TEST_NAME+'.bak',
                         'add ext if none in the original including a path')
        ans = changeExt(SIMPLE_TEST_NAME+'.ext','.bak')
        self.assertEqual(ans, SIMPLE_TEST_NAME+'.ext',
                         'not change if there is an ext in the original')
        ans = changeExt(SIMPLE_TEST_NAME+'.ext','.bak', True)
        self.assertEqual(ans, SIMPLE_TEST_NAME+'.bak',
                         'change regardless if override is True ')
        

from os import path
# show what is being tested and from where - pick one depending on need
print('\nTesting changeExt in module:\n',path.abspath(fileUtils.__file__))

if __name__=='__main__':
    unittest.main()
    
