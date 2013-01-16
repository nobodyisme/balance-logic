# -*- coding: utf-8 -*-

import unittest
import testEmptySet
import testNormalSet

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testEmptySet.TestEmptySets))
    suite.addTest(unittest.makeSuite(testNormalSet.TestNormalSets))
    unittest.TextTestRunner(verbosity=2).run(suite)