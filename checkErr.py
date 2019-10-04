"""
Created by Christian Montero, Tanmay Bhoir, William DeRoberts, Shoaib Sherwani
September 16, 2019
This file uses python3.6 to check errors within gedcom files
"""
import unittest
from datetime import datetime, date

## US01 Checks for dates in the future (Tanmay)
def checkCurrDate(fam, count, errLog, ind):
    current = datetime.now().date()
    error = False
    err_line =""
  
    if fam != []:
        marrDate = fam.married
        divDate = fam.divorced

        if marrDate > current:
            err_line = "ERROR: FAMILY: US01: Marriage Date (%s) of %s (%s) is after the current date *** families index %d"
            print(err_line % (marrDate, fam.husbandName, fam.husband, count))
            errLog.append(err_line)
            error = True
            return error

        if divDate != 'NA':
            if divDate > current:
                err_line = "ERROR: FAMILY: US01: Divorce Date (%s) of %s (%s) is after the current date (gedcom line %d)"
                print(err_line % (divDate, fam.husbandName, fam.husband, count))
                errLog.append(err_line)
                error = True
                return error
    
    if ind != []:
        if ind.birthday > current:
            err_line = "ERROR: INDIVIDUAL: US01: Birth Date (%s) of %s (%s) is after the current date *** individuals index %d"
            print(err_line % (ind.birthday, ind.name, ind.id, count))
            errLog.append(err_line)
            error = True    
            return error

        if ind.alive == 'False' and ind.death > current:
            err_line = "ERROR: INDIVIDUAL: US01: Death Date (%s) of %s (%s) is after the current date *** individuals index %d"
            print(err_line % (ind.death, ind.name, ind.id, count))
            errLog.append(err_line)
            error = True
            return error 
    
    return error

## US02 Checks Birth and Marriage Dates - Ensures Birth before Marriage (William)
def checkBirth_marriage(fam, count, errLog, individuals):
    error = False
    marrDate = fam.married
    husbID = fam.husband
    wifeID = fam.wife

    for ind in individuals:
        if (ind.id == husbID):
            husbName = ind.name
            husbBday = ind.birthday

            if husbBday > marrDate:
                errLine = "ERROR: FAMILY: US02: %s's (%s) birthday (%s) is after his marriage date (%s) *** families index %d"
                print(errLine % (husbName, husbID, husbBday, marrDate, count))
                errLog.append("ERROR: FAMILY: US02: " + husbName + "(" + husbID + ") birthday (" + str(husbBday) + ") is after his marriage date (" + str(marrDate) + ") *** families index " + str(count))
                error = True
                return error
        
        if (ind.id == wifeID):
            wifeName = ind.name
            wifeBday = ind.birthday

            if wifeBday > marrDate:
                errLine = "ERROR: FAMILY: US02: %s's (%s) birthday (%s) is after her marriage date (%s) *** families index %d"
                print(errLine % (wifeName, wifeID, wifeBday, marrDate, count))
                errLog.append("ERROR: FAMILY: US02: " + wifeName + "(" + wifeID + ") birthday (" + str(wifeBday) + ") is after his marriage date (" + str(marrDate) + ") *** families index " + str(count))
                error = True
                return error 
    
    return error

## US03 Checks Birth and Death dates - Ensures Birth before Death (William)
def checkBirth_death(ind, count, errLog):
    error = False
    err_line = ""
    if ((ind.alive == "False") and (ind.death < ind.birthday)):
        indName = ind.name
        indID = ind.id
        errLine = "ERROR: INDIVIDUAL: US03: %s's (%s) death (%s) is prior their birth (%s) *** individuals index %d"
        print(errLine % (indName, indID, ind.death, ind.birthday, count))
        errLog.append("ERROR: INDIVIDUAL: US03: " + indName + "(" + indID + ") death (" + str(ind.death) + "is prior to their birth (" + str(ind.birthday) + ") *** individuals index " + str(count))
        error = True
        return error

## US04 Checks Marriage and Divorce dates - Ensures Marriage before Divorce (Tanmay)
def checkMarrBeforeDiv(fam, count, errLog):
    error = False
    err_line =""
    husbID = fam.husband
    husbName = fam.husbandName
    married = fam.married
    divorced = fam.divorced
    if divorced != 'NA':
        if married > divorced:
            err_line = "ERROR: FAMILY: US04: Divorce Date (%s) of %s (%s) was before his date of marriage (%s) *** families index %d"
            print(err_line % (divorced, husbName, husbID, married, count))
            errLog.append(err_line)
            error = True
            return error
    
    return error

## US05 Checks Marriage and Death dates - Ensures Marriage before Death (Shoaib)
def checkMarriage(fam, count, errLog, ind):
    error = False
    err_line =""
    for i in ind:
        married = fam.married
        death = i.death
        if fam.husband == i.id or fam.wife == i.id:
            if i.alive == "False" and married:
                ind_name = i.name
                ind_id = i.id
                line_loc = count
                if married >= death:
                    err_line = "ERROR: FAMILY: US05: Marriage Date (%s) of %s (%s) was greater than or equal to date of death (%s) *** families index %d"
                    print(err_line % (married, ind_name, ind_id, death, line_loc))
                    errLog.append(err_line)
                    error = True
                    return error
    return error

## US06 Checks Divorce and Death dates - Ensures Divorce before Death (Shoaib)
def checkDivorce(fam, count, errLog, ind):
    error = False
    err_line =""
    for i in ind:
        divorce = fam.divorced
        death = i.death
        if i.alive == 'False' and death != 'NA' and divorce != 'NA':
            ind_name = i.name
            ind_id = i.id
            line_loc = count
            if divorce >= death:
                err_line = "ERROR: FAMILY: US06: Divorce Date (%s) of %s (%s) was greater than or equal to date of death (%s) *** families index %d"
                print(err_line % (divorce, ind_name, ind_id, death, line_loc))
                errLog.append(err_line)
                error = True
                return error
   
    return error

## US07 Checks for indivduals with age greater than 150 (Christian)
def checkAge(ind, count, errLog):
    error = False
    if (ind.alive) and ((ind.age) >= 150):
        indName = ind.name
        indID = ind.id
        errLine = "ERROR: INDIVIDUAL: US07: Age of %s (%s) is greater than or equal to 150 years *** individuals index %d"
        print(errLine % (indName, indID, count))
        errLog.append("ERROR: INDIVIDUAL: US07: Age of " + indName + "(" + indID + ") " + "is greater than or equal to 150 years *** individuals index " + str(count))
        error = True
        return error

    elif (ind.alive is False) and (ind.age >= 150):
        indName = ind.name
        indID = ind.id
        lineLoc = count
        errLine = "ERROR: INDIVIDUAL: US07: Age of %s (%s) was greater than or equal to 150 years at death *** individuals index %d"
        print(errLine % (indName, indID, lineLoc))
        errLog.append("ERROR: INDIVIDUAL: US07: Age of " + indName + "(" + indID + ") " + "was greater than or equal to 150 years at death *** individuals index " + str(count))
        error = True
        return error
    
    return error

## US08 Checks Birth Dates of Individual and Marriage Dates of Parents - Ensures Parent Marriage before Child Birth
def checkBirth_parentMarriage(fam, count, errLog, individuals):
    error = False
    marrDate = fam.married
    children = fam.children

    for child in children:
        for ind in individuals:
            if (ind.id == child) and (ind.birthday < marrDate):
                errLine = "ERROR: FAMILY: US08: %s's (%s) birthday (%s) is after his parent's marriage date (%s) *** families index %d"
                print(errLine % (ind.name, ind.id, ind.birthday, marrDate, count))
                errLog.append("ERROR: FAMILY: US08: " + ind.name + "(" + ind.id + ") birthday (" + str(ind.birthday) + ") is after their parents marriage date (" + str(marrDate) + ") *** families index " + str(count))
                error = True
                return error
    
    return error

## US09 Checks Child Birth Before Parent Death

## US10 Checks Parents Are at Least 14 Years Old

## US11 Checks Divorce Before Re-Marriage

## US12 Checks Mother is Less Than 60 Years and Father is Less Than 80 Years Old

## US13 Checks Sibling Birth Dates are More Than 8 Months or Less Than 2 Days Apart

## US14 Checks Less Than or Equal to 5 Siblings with Same Birth Date
def checkMultipleBirths(fam, count, errLog, individuals):
    error = False
    children = fam.children
    birthdays = {}

    for child in children:
        for ind in individuals:
            if child == ind.id:
                bday = ind.birthday
                if bday not in birthdays:
                    birthdays[bday] = 1
                else:
                    birthdays[bday] += 1 

                    if birthdays[bday] > 5:
                        errLine = "ERROR: FAMILY: US14: %s and %s have more than 5 children with the same birth date of %s (%d children) *** families index %d"
                        print(errLine % (fam.husbandName, fam.wifeName, bday, birthdays[bday], count))
                        errLog.append("ERROR: FAMILY: US14: " + fam.husbandName + " and " + fam.wifeName + " have more than 5 children with the same birth date of " + str(bday) + "(" + str(birthdays[bday]) + " children) *** families index " + str(count))
                        error = True
                        return error

## US15 Checks There Are Less Than 15 Siblings In One Family
def checkSiblingCount(fam, count, errLog):
    error = False
    children = fam.children
    if (len(children) > 15):
        errLine = "ERROR: FAMILY: US15: %s and %s have more than 15 children (%d children) *** families index %d"
        print(errLine % (fam.husbandName, fam.wifeName, len(children), count))
        errLog.append("ERROR: FAMILY: US15: " + fam.husbandName + " and " + fam.wifeName + " have more than 15 children (" + str(len(children)) + " children) *** families index " + str(count))
        error = True
        return error


## US16 Checks All Males in Same Family Share Same Surname