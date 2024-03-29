"""
Created by Christian Montero, Tanmay Bhoir, William DeRoberts, Shoaib Sherwani
September 16, 2019
This file uses python3.6 to check errors within gedcom files
"""
import unittest
import re
import collections
from datetime import datetime, timedelta
from dateutil import relativedelta as rdelta


########################################################################
############################### SPRINT 1 ###############################
########################################################################

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
            errLog.append("ERROR: FAMILY: US01: Marriage Date (" + str(marrDate) + ") of " + fam.husbandName + " (" + fam.husband + ") is after the current date *** families index " + str(count))
            error = True
            return error

        if divDate != 'NA':
            if divDate > current:
                err_line = "ERROR: FAMILY: US01: Divorce Date (%s) of %s (%s) is after the current date (gedcom line %d)"
                print(err_line % (divDate, fam.husbandName, fam.husband, count))
                errLog.append("ERROR: FAMILY: US01: Divorce Date (" + str(divDate) + " ) of" + fam.husbandName + " (" + fam.husband + ") is after the current date *** families index " + str(count))
                error = True
                return error
    
    if ind != []:
        if ind.birthday > current:
            err_line = "ERROR: INDIVIDUAL: US01: Birth Date (%s) of %s (%s) is after the current date *** individuals index %d"
            print(err_line % (ind.birthday, ind.name, ind.id, count))
            errLog.append("ERROR: INDIVIDUAL: US01: Birth Date (" + ind.birthday + ") of " + ind.name + " (" + str(ind.id) + ") is after the current date *** individuals index " + str(count))
            error = True    
            return error

        if ind.alive == 'False' and ind.death > current:
            err_line = "ERROR: INDIVIDUAL: US01: Death Date (%s) of %s (%s) is after the current date *** individuals index %d"
            print(err_line % (ind.death, ind.name, ind.id, count))
            errLog.append("ERROR: INDIVIDUAL: US01: Death Date (" + str(ind.death) + ") of " + ind.name + " (" + str(ind.id) + ") is after the current date *** individuals index " + str(count))
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
            errLog.append("ERROR: FAMILY: US04: Divorce Date (" + str(divorced) + ") of " + str(husbName) + " (" + str(husbID) + ") was before his date of marriage (" + str(married) + ") *** families index" + str(count) + ")")
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
                    errLog.append("ERROR: FAMILY: US05: Marriage Date (" + str(married) + ") of " + ind_name + " (" + str(ind_id) + ") was greater than or equal to date of death (" + str(death) + ") *** families index " + str(count))
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
                errLog.append("ERROR: FAMILY: US06: Divorce Date (" + str(divorce) + ") of " + ind_name + " (" + str(ind_id) + ") was greater than or equal to date of death (" + str(death) + ") *** families index " + str(line_loc))
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

## US08 Checks Birth Dates of Individual and Marriage Dates of Parents - Ensures Parent Marriage before Child Birth (Christian)
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



########################################################################
############################### SPRINT 2 ###############################
########################################################################

## US09 Checks Child Birth Before Parent Death (Willy D)
def checkBirthBeforeParentDeath(fam, count, errLog, individuals):
    error = False
    dadID = fam.husband
    momID = fam.wife
    children = fam.children

    dadDead = False
    momDead = False

    for ind in individuals:
            if ind.id == dadID:
                if ind.alive == "False":
                    dadDead = True
                    dadDeathDate = ind.death
            if ind.id == momID:
                if ind.alive == "False":
                    momDead = True
                    momDeathDate = ind.death

    for ind in individuals:
        if ind.id in children:
            if dadDead:
                if ind.birthday > dadDeathDate:
                    errLine = "ERROR: FAMILY: US09: %s's (%s) birthday (%s) is after their father's death date (%s) *** families index %d"
                    print(errLine % (ind.name, ind.id, str(ind.birthday), str(dadDeathDate), count))
                    errLog.append("ERROR: FAMILY: US09: " + ind.name + "(" + ind.id + ") birthday (" + str(ind.birthday) + ") is before their father's death date (" + str(dadDeathDate) + ") *** families index " + str(count))
                    error = True
            if momDead:
                if ind.birthday > momDeathDate:
                    errLine = "ERROR: FAMILY: US09: %s's (%s) birthday (%s) is after their mother's death date (%s) *** families index %d"
                    print(errLine % (ind.name, ind.id, str(ind.birthday), str(momDeathDate), count))
                    errLog.append("ERROR: FAMILY: US09: " + ind.name + "(" + ind.id + ") birthday (" + str(ind.birthday) + ") is before their mother's death date (" + str(momDeathDate) + ") *** families index " + str(count))
                    error = True
    
    return error

## US10 Checks Parents Are at Least 14 Years Old (Tanmay)
def checkMarrAfter14(individuals, fam, count, errLog):
    error = False
    if fam != []:
        for ind in individuals:
            if ind.id in fam.husband or ind.id in fam.wife:
                if ind.age < 14:
                    errLine = "ERROR: FAMILY: US10: %s (%s) is married on (%s) and his age (%d) is less than 14 years*** families index %d"
                    print(errLine % (ind.name, ind.id, fam.married, ind.age, count))
                    errLog.append("ERROR: FAMILY: US10: " + ind.name  + " (" + str(ind.id) + ") is married on (" + str(fam.married) + ") and his age (" + str(ind.age) + ") is less than 14 years *** families index " + str(count))
                    error = True
        
        return error

## US11 Checks Divorce Before Re-Marriage (Willy D)
def checkDivorcebeforeRemarriage(fam, count, errLog, families):
    error = False
    
    if fam.divorced != "NA":
        divorceDate = fam.divorced
        husbandID = fam.husband
        wifeID = fam.wife
        for f in families:
            if fam.id != f.id:
                if f.husband == husbandID:
                    if f.married < divorceDate:
                        errLine = "ERROR: FAMILY: US11: %s's (%s) re-marriage (%s) is before his divorce date (%s) *** families index %d"
                        print(errLine % (f.husbandName, husbandID, str(f.married), str(divorceDate), count))
                        errLog.append("ERROR: FAMILY: US11: " + f.husbandName + "(" + husbandID + ") re-marriage (" + str(f.married) + ") is before his divorce date (" + str(divorceDate) + ") *** families index " + str(count))
                        error = True
                        
                if f.wife == wifeID:
                    if f.married < divorceDate:
                        errLine = "ERROR: FAMILY: US11: %s's (%s) re-marriage (%s) is before her divorce date (%s) *** families index %d"
                        print(errLine % (f.wifeName, wifeID, str(f.married), str(divorceDate), count))
                        errLog.append("ERROR: FAMILY: US11: " + f.wifeName + "(" + wifeID + ") re-marriage (" + str(f.married) + ") is before her divorce date (" + str(divorceDate) + ") *** families index " + str(count))
                        error = True
    return error

## US12 Mother should be less than 60 years older than her children and father should be
# less than 80 years older than his children (Shoaib)
def marriage_age(fam, count, errLog, individuals):
    error = False
    children=fam.children
    husband=fam.husband
    father_bday=None
    mother_bday=None
    wife=fam.wife
    for ind in individuals:
        if ind.id == husband and ind.birthday is not None and ind.gender == 'M':
            father_bday=ind.birthday
        elif ind.id == wife and ind.birthday is not None and ind.gender == 'F':
            mother_bday=ind.birthday
        elif father_bday is not None and mother_bday is not None:
            break
    if len(children) > 0:
        for child in children:
            for ind in individuals:
                if ind.id == child and ind.birthday is not None:
                    diff_mother=rdelta.relativedelta(ind.birthday, mother_bday)
                    diff_father=rdelta.relativedelta(ind.birthday, father_bday)
                    if diff_mother.years > 60:
                        errLine = "ERROR: FAMILY: US12: %s and %s Mother was birth date %s " \
                                "and child birth date %s has difference %s more than 60 year difference " \
                                "*** families index %d"
                        print(errLine % (fam.husbandName, fam.wifeName, mother_bday, ind.birthday, diff_mother.years,
                                         count))
                        errLog.append(
                            "ERROR: FAMILY: US12: " + fam.husbandName + " and " + fam.wifeName +
                            "Mother was birth date " + str(mother_bday) + "and child birth date" + str(ind.birthday) +
                            " has difference"+ str(diff_mother.year) + "more than 60 year difference *** families index"
                            + str(count))
                        error = True
                    elif diff_father.years > 80:
                        errLine = "ERROR: FAMILY: US12: %s and %s Father was birth date %s " \
                                "and child birth date %s has difference %d more than 80 year difference " \
                                "*** families index %d"
                        print(errLine % (fam.husbandName, fam.wifeName, father_bday, ind.birthday, diff_mother.years,
                                         count))
                        errLog.append(
                            "ERROR: FAMILY: US12: " + fam.husbandName + " and " + fam.wifeName +
                            "Father was birth date " + str(father_bday) + "and child birth date" + str(ind.birthday) +
                            " has difference" + str(
                                diff_mother.year) + "more than 80 year difference *** families index"
                            + str(count))
                        error = True
        return error

## US13 Checks Sibling Birth Dates are More Than 8 Months or Less Than 2 Days Apart (Shoaib)
def siblingspaces(fam, count, errLog, individuals):
    error = False
    children = fam.children
    sib_birthdays = []
    i = 0

    if len(children) > 1:
        for child in children:
            for ind in individuals:
                if ind.birthday is not None and ind.id == child:
                    sib_birthdays.append(ind.birthday)
        count1 = len(sib_birthdays)
        while i < count1 - 1:
            diff = rdelta.relativedelta(sib_birthdays[i + 1], sib_birthdays[i])
            if diff.days > 2  or diff.months < 8:
                errLine = "ERROR: FAMILY: US13: %s and %s have 2 children with birthdates less than 2 days apart (twins) birth or are more than more than 8 months apart of %s and %s *** families index %d"
                print(errLine % (fam.husbandName, fam.wifeName, sib_birthdays[i + 1], sib_birthdays[i], count))
                errLog.append(
                    "ERROR: FAMILY: US13: " + fam.husbandName + " and " + fam.wifeName + " have 2 children with birthdates less than 2 days apart (twins) birth date of" + str(
                        sib_birthdays[i + 1]) + "(" + str(sib_birthdays[i]) + " children) *** families index " + str(
                        count))
                error = True
            i += 1
        return error
    return error

## US14 Checks Less Than or Equal to 5 Siblings with Same Birth Date (Christian)
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

## US15 Checks There Are Less Than 15 Siblings In One Family (Christian)
def checkSiblingCount(fam, count, errLog):
    error = False
    children = fam.children
    if (len(children) > 15):
        errLine = "ERROR: FAMILY: US15: %s and %s have more than 15 children (%d children) *** families index %d"
        print(errLine % (fam.husbandName, fam.wifeName, len(children), count))
        errLog.append("ERROR: FAMILY: US15: " + fam.husbandName + " and " + fam.wifeName + " have more than 15 children (" + str(len(children)) + " children) *** families index " + str(count))
        error = True
        return error

## US16 Checks All Males in Same Family Share Same Surname (Tanmay)
def male_last_name(fam, count, errLog, individuals):
    error = False
    name_l = []
    children = fam.children
    for child in children:
        for ind in individuals:
            if ind.gender == "M" and ind.id == child:
                name_l.append(str(ind.name))
    for name in name_l[1:]:
        match_last_name1 = re.search(r"/(.*)/", (" ".join(name)))
        match_last_name2 = re.search(r"/(.*)/", (" ".join(name_l[0])))
        if match_last_name1 and match_last_name2 and match_last_name1.group(1) != match_last_name2.group(1):
            errLine="ERROR: FAMILY: US16: %s and %s have 1 Male in their family with different last names %s and %s " \
                    "*** families index %d "
            print(errLine % (fam.husbandName, fam.wifeName, name, name[0], count))
            errLog.append(
                "ERROR: FAMILY: US16: " + fam.husbandName + " and " + fam.wifeName + 'have 1 Male in their family '
                                                                                     'with different last names ' +
                name + "and " + name[0] + " *** families index " + str(
                    count))
            error = True
    return error


########################################################################
############################### SPRINT 3 ###############################
########################################################################

## US17 Parents should not marry any of their children (Tanmay)
def checkNoMarrChild(fam, count, errLog, families):
    error = False
    if fam.husband in fam.children:
        errLine = "ERROR: FAMILY: US17: %s (%s) and %s (%s) are married but have a parent-child relation *** families index %d"
        print(errLine % (fam.husbandName, fam.husband, fam.wifeName, fam.wife, count))
        errLog.append("ERROR: FAMILY: US17: " + fam.husbandName + " (" + fam.husband + ") and " + fam.wifeName + " (" + fam.wife + ") are married but have a parent-child relation *** families index " + str(count))
        error = True
    elif fam.wife in fam.children:
        errLine = "ERROR: FAMILY: US17: %s (%s) and %s (%s) are married but have a parent-child relation *** families index %d"
        print(errLine % (fam.husbandName, fam.husband, fam.wifeName, fam.wife, count))
        errLog.append("ERROR: FAMILY: US17: " + fam.husbandName + " (" + fam.husband + ") and " + fam.wifeName + " (" + fam.wife + ") are married but have a parent-child relation *** families index " + str(count))
        error = True
    return error

## US18 Siblings should not marry one another (Tanmay)
def checkNoSiblingsMarry(fam, count, errLog, families):
    error = False
    if siblings(fam.husband, fam.wife, families):
        errLine = "ERROR: FAMILY: US18: %s (%s) and %s (%s) are siblings and married to each other *** families index %d"
        print(errLine % (fam.husbandName, fam.husband, fam.wifeName, fam.wife, count))
        errLog.append("ERROR: FAMILY: US18: " + str(fam.husbandName) + " and " + str(fam.wifeName) + " are siblings and married *** families index " + str(count))
        error = True
    return error
def parents(personID, families):
    parents = []
    for family in families:
        if personID in family.children:
            parents = [family.husband, family.wife]
            return parents
    return parents
def siblings(husbID, wifeID, families):
    paternal = parents(husbID, families)
    maternal = parents(wifeID, families)
    for comm1 in paternal:
        for comm2 in maternal:
            if comm1 == comm2:
                return True
    return False
   

## US19 First cousins should not marry one another (Willy D)
def checkCousinsMarried(fam, count, errLog, families):
    error = False
    if areCousins(fam.husband, fam.wife, families):
        errLine = "ERROR: FAMILY: US19: %s and %s are cousins and married *** families index %d"
        print(errLine % (fam.husbandName, fam.wifeName, count))
        errLog.append(
            "ERROR: FAMILY: US19: " + str(fam.husbandName) + " and " + str(fam.wifeName) + " are cousins and married *** families index " + str(count))
        error = True

    return error
def getParents(personID, families):
    parents = []
    for f in families:
        if personID in f.children:
            parents = [f.husband, f.wife]
            return parents

    return parents
def areCousins(husbandID, wifeID, families):
    husbandParents = getParents(husbandID, families)
    husbandGrandparents = []
    if husbandParents != []:
        husbandGrandparents = getParents(husbandParents[0], families) + getParents(husbandParents[1], families)

    wifeParents = getParents(wifeID, families)
    wifeGrandparents = []
    if wifeParents != []:
        wifeGrandparents = getParents(wifeParents[0], families) + getParents(wifeParents[1], families)

    for i in husbandGrandparents:
        for j in wifeGrandparents:
            if i == j:
                return True

    return False

## US20 Aunts and uncles should not marry their nieces or nephews (Willy D)
def checkMarriedtoAuntUncle(fam, count, errLog, families):
    error = False
    if isAuntOrUncle(fam.husband, fam.wife, families):
        errLine = "ERROR: FAMILY: US20: %s is married to his aunt %s *** families index %d"
        print(errLine % (fam.husbandName, fam.wifeName, count))
        errLog.append(
            "ERROR: FAMILY: US20: " + str(fam.husbandName) + " is married to his aunt " + str(fam.wifeName) + "*** families index " + str(count))
        error = True
    elif isAuntOrUncle(fam.wife, fam.husband, families):
        errLine = "ERROR: FAMILY: US20: %s is married to her uncle %s *** families index %d"
        print(errLine % (fam.wifeName, fam.husbandName, count))
        errLog.append(
            "ERROR: FAMILY: US20: " + str(fam.wifeName) + " is married to her uncle  " + str(fam.husbandName) + "*** families index " + str(count))
        error = True

    return error

def isAuntOrUncle(person1ID, person2ID, families):
    person1Parents = getParents(person1ID, families)
    person1Grandparents = []
    if person1Parents != []:
        person1Grandparents = getParents(person1Parents[0], families) + getParents(person1Parents[1], families)

    person2Parents = getParents(person2ID, families)

    for i in person1Grandparents:
        for j in person2Parents:
            if i == j and (j not in person1Parents):
                return True
    return False

## US21 Husband in family should be male and wife in family should be female (Shoaib)
def gender_role_check(fam, count, errLog, individuals):
    error = False
    husband = fam.husband
    wife = fam.wife

    for ind in individuals:
        if wife == ind.id and ind.gender != 'F':
            errLine="ERROR: FAMILY: US21: %s is wife marked Male %s as an individual " \
                    "*** families index %d "
            print(errLine % (fam.wifeName, ind.gender, count))
            errLog.append(
                "ERROR: FAMILY: US21: " + fam.wifeName + " is wife marked Male " + ind.gender + 'as an individual' +
                "*** families index " + str(count))
            error = True
        elif husband == ind.id and ind.gender != 'M':
            errLine="ERROR: FAMILY: US21: %s is husband marked Female %s as an individual " \
                    "*** families index %d "
            print(errLine % (fam.husbandName, ind.gender, count))
            errLog.append(
                "ERROR: FAMILY: US21: " + fam.wifeName + " is wife marked Male " + ind.gender + 'as an individual' +
                "*** families index " + str(count))
            error = True
    return error

## US22 All individual IDs should be unique and all family IDs should be unique (Shoaib)
def unique_id_check(families, errLog, individuals):

    ind_error = []
    fam_error = []
    fid = {}
    iid = {}
    count = 0
    for fam in families:
        count+=1
        if fam.id not in fid:
            fid[fam.id] = 1
            fam_error.append(False)
        else:
            errLine= "ERROR: FAMILY: US22: Family ID %s is not unique *** Family index %d"
            print(errLine % (fam.id, count))
            errLog.append("ERROR: FAMILY: US22: Family ID" + fam.id + "is not unique *** families index " + str(count))
            fam_error.append(True)

    count = 0
    for ind in individuals:
        count+=1
        if ind.id not in iid:
            iid[ind.id] = 1
            ind_error.append(False)
        else:
           errLine="ERROR: INDIVIDUAL: US22: Individual ID %s is not unique *** individuals index %d"
           print(errLine % (ind.id, count))
           errLog.append("ERROR: INDIVIDUAL: US22: Individual ID" + ind.id + "is not unique *** Individual index " + str(count))
           ind_error.append(True)
    
    return [ind_error, fam_error]

## US23 No more than one individual with the same name and birth date should appear in a GEDCOM file (Christian)
def check_duplicate_names_birthdays(ind, individuals, count, errLog):
    error = False
    inst = 0
    name = ind.name
    birth = ind.birthday

    for i in individuals:
        if i.name == name and i.birthday == birth:
            inst += 1
            if inst > 1:
                errLine = "ERROR: FAMILY: US23: There are more than one individuals with name %s and birthdate %s *** individuals index %d"
                print(errLine % (name, birth, count))
                errLog.append("ERROR: FAMILY: US23: There are more than one individuals with name " + name + " and birthdate " + str(birth) +  " *** individuals index " + str(count))
                error = True
                return error

## US24 No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file (Christian)
def check_multi_family_parent(fam, count, errLog, families):
    error = False
    husband = fam.husbandName
    husbandID = fam.husband
    wife = fam.wifeName
    wifeID = fam.wife
    date = fam.married
    refHus = 0
    refWif = 0

    for f in families:
        if (wife == f.wifeName and date == f.married):
            refWif += 1
            if refWif > 1:
                errLine = "ERROR: FAMILY: US24: %s (%s) is also in family %s with the same marriage date (%s) *** families index %d"
                print(errLine % (wife, wifeID, f.id, date, count))
                errLog.append("ERROR: FAMILY: US24: " + wife + " (" + wifeID + ") is also in family " + str(f.id) + " with the same marriage date (" + str(date) + " *** individuals index " + str(count))
                error = True
                return error

        if (husband == f.husbandName and date == f.married):
            refHus += 1
            if refHus > 1:
                errLine = "ERROR: FAMILY: US24: %s (%s) is also in family %s with the same marriage date (%s) *** families index %d"
                print(errLine % (husband, husbandID, f.id, date, count))
                errLog.append("ERROR: FAMILY: US24: " + husband + " (" + husbandID + ") is also in family " + str(f.id) + " with the same marriage date (" + str(date) + ") *** individuals index " + str(count))
                error = True
                return error

    return error


########################################################################
############################### SPRINT 4 ###############################
########################################################################

# US 30 Check Married People Alive
def check_isalive(husbandName, wifeName, individuals):
    husbandAlive = None
    wifeAlive = None
    for ind in individuals:
        if husbandName == ind.name and ind.alive == 'True':
            husbandAlive = True
        elif wifeName == ind.name and ind.alive == 'True':
            wifeAlive = True
    return  husbandAlive, wifeAlive

# US25 - Unique First Names & DOB in Families
def check_unique_family_names_dob(fam, count, errLog, individuals):
    error = False
    children = fam.children
    names = {}
        
    for child in children:
        if child == 'NA':
            continue
        else:
            for ind in individuals:
                if (child == ind.id) and (ind.name not in names):
                    names[ind.name] = str(ind.birthday)
                elif (child == ind.id) and (ind.name in names) and (names[ind.name] == str(ind.birthday)):
                    errLine = "ERROR: FAMILY: US25: %s (%s) has one or more siblings with the same name and birthdate (%s) *** families index %d"
                    print(errLine % (ind.name, ind.id, ind.birthday, count))
                    errLog.append("ERROR: FAMILY: US25: " + ind.name + " (" + ind.id + ") has one or more siblings with the same name and birthdate (" + str(ind.birthday) + ") *** families index " + str(count))
                    error = True
                    return error
                    
                
        

