# -*- coding: utf-8 -*-

import generators
import balancelogic
import unittest

class TestEmptySets(unittest.TestCase):
    def setUp(self):
        unit = generators.normal_unit()
        unit.set(pisBad = True)
        self.__all_units = [unit]
        
    def test_EmptySet(self):
        self.assertRaises(IndexError, balancelogic.rawBalance, [], generators.default_balance_directives())
    
    def test_OnlyBad(self):
        self.assertRaises(IndexError, balancelogic.rawBalance, self.__all_units, generators.default_balance_directives())

if __name__ == "__main__":
    unittest.main()