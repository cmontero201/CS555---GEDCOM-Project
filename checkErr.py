"""
Created by Christian Montero, Tanmay Bhoir, William DeRoberts, Shoaib Sherwani
September 16, 2019
This file uses python3.6 to check errors within gedcom files
"""
import unittest

## US07 Checks for indivduals with age greater than 150 (Christian)
def checkAge(ind, count, errLog):
    error = False
    if (ind.alive) and ((ind.age) >= 150):
        indName = ind.name
        indID = ind.id
        errLine = "ERROR US07: Age of %s (%s) is greater than or equal to 150 years (individuals line %d)"
        print(errLine % (indName, indID, count))
        errLog.append("ERROR US07: Age of " + indName + "(" + indID + ") " + "is greater than or equal to 150 years (individuals index " + str(count) + ")")
        error = True
        return error

    elif (ind.alive is False) and (ind.age >= 150):
        indName = ind.name
        indID = ind.id
        lineLoc = count
        errLine = "ERROR US07: Age of %s (%s) was greater than or equal to 150 years at death (individuals line %d)"
        print(errLine % (indName, indID, lineLoc))
        errLog.append("ERROR US07: Age of " + indName + "(" + indID + ") " + "was greater than or equal to 150 years at death (individuals index " + str(count) + ")")
        error = True
        return error

## US08 Checks Birth and Marriage Dates - Ensures Birth before Marriage (Christian)
def checkBirth_marriage(fam, count, errLog, individuals):
    error = False
    marrDate = fam.married
    husbID = fam.husband
    wifeID = fam.wife

    for ind in individuals:
        if (ind.id == husbID):
            husbName = ind.name
            husbBday = ind.birthday
        
        if (ind.id == wifeID):
            wifeName = ind.name
            wifeBday = ind.birthday

    if husbBday > marrDate:
        errLine = "ERROR US08: %s's (%s) birthday is after his marriage date (families line %d)"
        print(errLine % (husbName, husbID, count))
        errLog.append("ERROR US08: " + husbName + "(" + husbID + ") birthday is after his marriage date (families index " + str(count) + ")")
        error = True
        return error

    if wifeBday > marrDate:
        errLine = "ERROR US08: %s's (%s) birthday is after her marriage date (families line %d)"
        print(errLine % (wifeName, wifeID, count))
        errLog.append("ERROR US08: " + wifeName + "(" + wifeID + ") birthday is after his marriage date (families index " + str(count) + ")")
        error = True
        return error
    


