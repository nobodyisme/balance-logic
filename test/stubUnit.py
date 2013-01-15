# -*- coding: utf-8 -*-

class StubUnit:
    def __init__(self,
                punitId = None,
                pdataType = None,
                prealPutPerPeriod = 1,
                pmaxPutPerPeriod = 5,
                prealGetPerPeriod = 1,
                pmaxGetPerPeriod = 5,
                pfreeSpaceInKb = 1048576,
                pfreeSpaceRelative = 0.99,
                pinService = False,
                pwriteEnable = True,
                pisBad = False):
        self.__unitId = punitId
        self.__dataType = pdataType
        self.__realPutPerPeriod = prealPutPerPeriod
        self.__maxPutPerPeriod = pmaxPutPerPeriod
        self.__realGetPerPeriod = prealGetPerPeriod
        self.__maxGetPerPeriod = pmaxGetPerPeriod
        self.__freeSpaceInKb = pfreeSpaceInKb
        self.__freeSpaceRelative = pfreeSpaceRelative
        self.__inService = pinService
        self.__writeEnable = pwriteEnable
        self.__isBad = pisBad
        

    def set(self,
                punitId = None,
                pdataType = None,
                prealPutPerPeriod = None,
                pmaxPutPerPeriod = None,
                prealGetPerPeriod = None,
                pmaxGetPerPeriod = None,
                pfreeSpaceInKb = None,
                pfreeSpaceRelative = None,
                pinService = None,
                pwriteEnable = None,
                pisBad = None):
        self.__unitId = punitId or self.__unitId
        self.__dataType = pdataType or self.__dataType
        self.__realPutPerPeriod = prealPutPerPeriod or self.__realPutPerPeriod
        self.__maxPutPerPeriod = pmaxPutPerPeriod or self.__maxPutPerPeriod
        self.__realGetPerPeriod = prealGetPerPeriod or self.__realGetPerPeriod
        self.__maxGetPerPeriod = pmaxGetPerPeriod or self.__maxGetPerPeriod
        self.__freeSpaceInKb = pfreeSpaceInKb or self.__freeSpaceInKb
        self.__freeSpaceRelative = pfreeSpaceRelative or self.__freeSpaceRelative
        self.__inService = pinService or self.__inService
        self.__writeEnable = pwriteEnable or self.__writeEnable
        self.__isBad = pisBad or self.__isBad


    def unitId(self):
        return self.__unitId
        
    def dataType(self):
        return self.__dataType
    
    def realPutPerPeriod(self):
        return self.__realPutPerPeriod
    
    def maxPutPerPeriod(self):
        return self.__maxPutPerPeriod
    
    def realGetPerPeriod(self):
        return self.__realGetPerPeriod
    
    def maxGetPerPeriod(self):
        return self.__maxGetPerPeriod
    
    def freeSpaceInKb(self):
        return self.__freeSpaceInKb
    
    def freeSpaceRelative(self):
        return self.__freeSpaceRelative

    def inService(self):
        return self.__inService

    def writeEnable(self):
        return self.__writeEnable

    def isBad(self):
        return self.__isBad
