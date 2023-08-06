"""
Unit test for the lsl.misc.wisdom module.
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
import sys
if sys.version_info < (3,):
    range = xrange
    
import os
import time
import warnings
import unittest
import numpy

from lsl.misc import wisdom


__version__  = "0.1"
__author__    = "Jayce Dowell"

class wisdom_tests(unittest.TestCase):
    """A unittest.TestCase collection of unit tests for the lsl.statistics.robust
    module."""
    
    def test_show(self):
        """Test wisdom.show()"""
        
        wisdom.show()


class wisdom_test_suite(unittest.TestSuite):
    """A unittest.TestSuite class which contains all of the lsl.misc.wisdom 
    units tests."""
    
    def __init__(self):
        unittest.TestSuite.__init__(self)
        
        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(wisdom_tests)) 


if __name__ == '__main__':
    unittest.main()
