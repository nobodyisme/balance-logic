# -*- coding: utf-8 -*-

import unittest
import testEmptySet

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(testEmptySet.TestEmptySets)
    unittest.TextTestRunner(verbosity=2).run(suite)