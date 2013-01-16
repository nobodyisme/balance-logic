# -*- coding: utf-8 -*-
import stubUnit
import json

balance_directives = json.load(open("balance_directives.json"))
counter = 1

def default_balance_directives():
    return balance_directives

def normal_unit(unitId = None, dataType = balance_directives["UnitDataType"]):
    if unitId is None:
        global counter
        unitId = counter
        counter += 1
    return stubUnit.StubUnit(
                             unitId,
                             dataType)
    
def unloaded_unit(unitId = None, dataType = balance_directives["UnitDataType"]):
    if unitId is None:
        global counter
        unitId = counter
        counter += 1
    return stubUnit.StubUnit(
                             unitId,
                             dataType,
                             prealPutPerPeriod = 0,
                             prealGetPerPeriod = 0)

def archive_unit(unitId = None, dataType = balance_directives["UnitDataType"]):
    if unitId is None:
        global counter
        unitId = counter
        counter += 1
    return stubUnit.StubUnit(
                             unitId,
                             dataType,
                             prealPutPerPeriod = 0)