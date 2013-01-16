# -*- coding: utf-8 -*-
import generators
import balancelogic
import unittest

class TestNormalSets(unittest.TestCase):
    def setUp(self):
        import copy
        self.__balance_directives = copy.copy(generators.default_balance_directives())
        self.__balance_directives["MinimumUnitsWithPositiveWeight"] = 10
        self.__balance_directives["AdditionalUnitsNumber"] = 3
        self.__balance_directives["AdditionalUnitsPercentage"] = 0.15
        self.__balance_directives["AdditionalMessagePerSecondNumber"] = 20
        self.__balance_directives["AdditionalMessagePerSecondPercentage"] = 0.15
        
    def test_NormalSet(self):
        import math
        units_set = []
        
        normal_units_count = 200
        archive_units_count = 100
        
        for n in range(normal_units_count):
            units_set.append(generators.normal_unit())
        for n in range(archive_units_count):
            units_set.append(generators.archive_unit())
        
        # reference object
        normal_unit = generators.normal_unit()
        
        putPerSecond = normal_unit.realPutPerPeriod() * normal_units_count
        putPerSecond = max(
            putPerSecond + self.__balance_directives["AdditionalMessagePerSecondNumber"],
            putPerSecond * (1 + self.__balance_directives["AdditionalMessagePerSecondPercentage"]))
        
        # the next line sometimes yealds a wrong value because of roundup problems
        position = math.ceil(putPerSecond / normal_unit.maxPutPerPeriod()) - 1
        position = max(
            position + self.__balance_directives["AdditionalUnitsNumber"],
            int(position * (1 + self.__balance_directives["AdditionalUnitsPercentage"])),
            self.__balance_directives["MinimumUnitsWithPositiveWeight"])
        # soft and hard positions are equal because of no step in space

        reference_cluster_statistics = {
            'PutMaxTotal': normal_unit.maxPutPerPeriod() * (normal_units_count + archive_units_count),
            'GetMaxTotal': normal_unit.maxGetPerPeriod() * (normal_units_count + archive_units_count),
            'GetRealTotal': normal_unit.realGetPerPeriod() * (normal_units_count + archive_units_count),
            'PutRealTotal': normal_unit.realPutPerPeriod() * normal_units_count,
            'UnitUsedNumber': normal_units_count + archive_units_count,
            'UnitUnusedNumber': 0,
            'HardPosition': position,
            'SoftPosition': position}
        
        reference_balance_result = {}
        for (current_position, unit) in enumerate(units_set):
            if current_position < position:
                reference_balance_result[unit.unitId()] = normal_unit.maxGetPerPeriod() *\
                        self.__balance_directives["WeightMultiplierHead"]
            else:
                reference_balance_result[unit.unitId()] = 0
         
        (balance_result, cluster_statistics) = balancelogic.rawBalance(units_set, self.__balance_directives)
        self.assertEqual(reference_cluster_statistics, cluster_statistics)
        self.assertEqual(reference_balance_result, balance_result)
    
if __name__ == "__main__":
    unittest.main() 