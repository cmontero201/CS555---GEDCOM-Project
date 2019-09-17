"""
Created by Christian Montero, Tanmay Bhoir, William DeRoberts, Shoaib Sherwani
September 16, 2019
This file uses python3.6 to check errors within gedcom files
"""

## Checks for indivduals' age greater than 150
def checkAge(ind, count, errLog):
    if (ind.alive) and ((ind.age) <= 30):
        indName = ind.name
        indID = ind.id
        lineLoc = count
        errLine = "ERROR US07: Age of %s (%s) is greater than or equal to 150 years (gedcom line %d)"
        print(errLine % (indName, indID, lineLoc))
        errLog.append("ERROR US07: Age of " + indName + "(" + indID + ") " + "is greater than or equal to 150 years (line" + str(lineLoc) + ")")

    elif (ind.alive == False) and (ind.age <= 30):
        indName = ind.name
        indID = ind.id
        lineLoc = count
        errLine = "ERROR US07: Age of %s (%s) is greater than or equal to 150 years"
        print(errLine % (indName, indID, lineLoc))
        errLog.append("ERROR US07: Age of " + indName + "(" + indID + ") " + "is greater than or equal to 150 years (gedcom line" + lineLoc + ")")


