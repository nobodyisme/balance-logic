# -*- coding: utf-8 -*-

def isAppropriateForBalance(unit, dataType, minimumFreeSpace, minimumFreeSpaceRelative):
    if (unit.inService()):
        return False
    if (not unit.writeEnable()):
        return False
    if (not dataType==unit.dataType()):
        return False
    if (minimumFreeSpace>unit.freeSpaceInKb()):
        return False
    if (minimumFreeSpaceRelative>unit.freeSpaceRelative()):
        return False
    if (unit.isBad()):
        return False
    return True

def getUnitListForBalance(unitOfDisksOnRowsList, dataType, minimumFreeSpace, minimumFreeSpaceRelative):
    unitListForBalance=[]
    unitListUnusedInBalance=[]
    for unit in unitOfDisksOnRowsList:
        if isAppropriateForBalance(unit, dataType, minimumFreeSpace, minimumFreeSpaceRelative):
            unitListForBalance.append(unit)
        else:
            unitListUnusedInBalance.append(unit)
    return (unitListForBalance, unitListUnusedInBalance)

def sortUnitListByFreespaceDesc(unitList):
    return sorted(unitList, key=lambda unit: unit.freeSpaceInKb(), reverse=True)

def getClusterStatistics(unitList):
    clusterLoad={}
    putRealTotal=0
    putMaxTotal=0
    getRealTotal=0
    getMaxTotal=0
    # need calculate stats for all disk also
    for unit in unitList:
        putRealTotal+=unit.realPutPerPeriod()
        putMaxTotal+=unit.maxPutPerPeriod()
        getRealTotal+=unit.realGetPerPeriod()
        getMaxTotal+=unit.maxGetPerPeriod()
        #print unit.freeSpaceInKb()
    clusterLoad["PutRealTotal"]=putRealTotal
    clusterLoad["PutMaxTotal"]=putMaxTotal
    clusterLoad["GetRealTotal"]=getRealTotal
    clusterLoad["GetMaxTotal"]=getMaxTotal
    return clusterLoad

def calculatePosition(sortedUnitList, balanceDirectives, clusterStatistics):
    mpsNumber=balanceDirectives["AdditionalMessagePerSecondNumber"]
    mpsPercentage=balanceDirectives["AdditionalMessagePerSecondPercentage"]
    additionalUnitsNumber=balanceDirectives["AdditionalUnitsNumber"]
    additionalUnitsPercentage=balanceDirectives["AdditionalUnitsPercentage"]
    putRealTotal=clusterStatistics["PutRealTotal"]
    putExpandedTotal=max(putRealTotal+mpsNumber, putRealTotal*(1+mpsPercentage))
    maxPutPartialSum=0.0
    position=0
    for (position, unit) in enumerate(sortedUnitList):
        maxPutPartialSum+=unit.maxPutPerPeriod()
        if (maxPutPartialSum>putExpandedTotal):
            break
    expandedPosition=max(
        position+additionalUnitsNumber
    ,   int(position*(1+additionalUnitsPercentage))
    ,   balanceDirectives["MinimumUnitsWithPositiveWeight"]
    )
    flatMode=1
    unit=None
    if 1==flatMode:
        unit=sortedUnitList[0]
    elif 2==flatMode:
        unit=sortedUnitList[expandedPosition]
    else:
        raise Exception("Only those flat modes supported")
    freeSpaceInKb=unit.freeSpaceInKb()
    tailHeightPercentage=balanceDirectives["TailHeightPercentage"]
    tailHeightSpaceInKb=balanceDirectives["TailHeightSpaceInKb"]
    freeSpaceInKbTailEnd=max(int(freeSpaceInKb*tailHeightPercentage), freeSpaceInKb-tailHeightSpaceInKb)
    softPosition=expandedPosition
    for (position, unit) in enumerate(sortedUnitList):
        if unit.freeSpaceInKb()<int(freeSpaceInKbTailEnd):
            softPosition=position
            break
    softPosition=max(expandedPosition, softPosition)
    return (expandedPosition, softPosition)

def smoothUnitsWeights(unitId2weight):
    upperRelativeThreshold=3
    unitIdWeightTupleList=filter(lambda e: e[1]!=0, list(unitId2weight.iteritems()))
    weightSum=sum(map(lambda e: e[1], unitIdWeightTupleList))
    weightAverage=weightSum/len(unitIdWeightTupleList)
    thresholdWeight=upperRelativeThreshold*weightAverage
    result={}
    for (unitId, weight) in unitId2weight.iteritems():
        if (weight<thresholdWeight):
            result[unitId]=weight
        else:
            result[unitId]=thresholdWeight
    return result

def calculateUnitWeights(sortedUnitList, balanceDirectives, positionTuple):
    (hardPosition, softPosition)=positionTuple
    unitId2weight={}
    weightMultiplierHead=balanceDirectives["WeightMultiplierHead"]
    weightMultiplierTail=balanceDirectives["WeightMultiplierTail"]
    minimumWeight=balanceDirectives["MinimumWeight"]
    for (position, unit) in enumerate(sortedUnitList):
        unitId=unit.unitId()
        maxGetPerPeriod=unit.maxGetPerPeriod()
        if position<hardPosition:
            weight=int(maxGetPerPeriod*weightMultiplierHead)
            unitId2weight[unitId]=max(weight, minimumWeight)
        elif position<softPosition:
            weight=int(maxGetPerPeriod*weightMultiplierTail)
            unitId2weight[unitId]=max(weight, minimumWeight)
        else:
            unitId2weight[unitId]=0
    return unitId2weight

def sumTwoDicts(first, second):
    names=set(first)&set(second)
    return dict((name, first.get(name)+second.get(name)) for name in names)

def rawBalance(unitOfDisksOnRowsList, balanceDirectives):
    mailUnitType=balanceDirectives["UnitDataType"]
    minimumFreeSpace=balanceDirectives["MinimumFreeSpaceInKbToParticipate"]
    minimumFreeSpaceRelative=balanceDirectives.get("MinimumFreeSpaceRelativeToParticipate", 0.0)
    unitListTuple=getUnitListForBalance(unitOfDisksOnRowsList, mailUnitType, minimumFreeSpace, minimumFreeSpaceRelative)
    (unitListForBalance, unitListUnusedInBalance)=unitListTuple
    unitListUnusedInBalance=filter(lambda e: mailUnitType==e.dataType(), unitListUnusedInBalance)
    unusedForPutClusterStatistics=getClusterStatistics(unitListUnusedInBalance)
    usedForPutClusterStatistics=getClusterStatistics(unitListForBalance)
    clusterStatistics=sumTwoDicts(usedForPutClusterStatistics, unusedForPutClusterStatistics)
    sortedUnitList=sortUnitListByFreespaceDesc(unitListForBalance)
    # MULCA-479 - this functions caclulate two positions
    positionTuple=calculatePosition(sortedUnitList, balanceDirectives, clusterStatistics)
    # MULCA-479 - this function calculate rawBalance units weights
    unitId2weight=calculateUnitWeights(sortedUnitList, balanceDirectives, positionTuple)
    unitId2weight=smoothUnitsWeights(unitId2weight)
    balanceInformation={
        "UnitUsedNumber" : len(unitListForBalance)
    ,   "UnitUnusedNumber" : len(unitListUnusedInBalance)
    ,   "HardPosition" : positionTuple[0]
    ,   "SoftPosition" : positionTuple[1]
    }
    balanceResult=dict(balanceInformation.items()+clusterStatistics.items())
    return (unitId2weight, balanceResult)
