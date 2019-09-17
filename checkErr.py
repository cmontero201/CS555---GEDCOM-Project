"""
Created by Christian Montero, Tanmay Bhoir, William DeRoberts, Shoaib Sherwani
September 16, 2019
This file uses python3.6 to check errors within gedcom files
"""
import unittest

## Checks for indivduals with age greater than 150
def checkAge(ind, count, errLog):
    error = False
    if (ind.alive) and ((ind.age) <= 30):
        indName = ind.name
        indID = ind.id
        lineLoc = count
        errLine = "ERROR US07: Age of %s (%s) is greater than or equal to 150 years (gedcom line %d)"
        print(errLine % (indName, indID, lineLoc))
        errLog.append("ERROR US07: Age of " + indName + "(" + indID + ") " + "is greater than or equal to 150 years (line" + str(lineLoc) + ")")
        error = True
        print(error)
        return error

    elif (ind.alive == False) and (ind.age <= 30):
        indName = ind.name
        indID = ind.id
        lineLoc = count
        errLine = "ERROR US07: Age of %s (%s) was greater than or equal to 150 years at death (gedcom line %d)"
        print(errLine % (indName, indID, lineLoc))
        errLog.append("ERROR US07: Age of " + indName + "(" + indID + ") " + "was greater than or equal to 150 years at death (gedcom line" + lineLoc + ")")
        error = True
        print(error)
        return error


