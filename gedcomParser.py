"""
Created by Christian Montero
Team Members: Tanmay Bhoir, William DeRoberts, Shoaib Sherwani
September 10, 2019
This file uses python3.6 to parse GEDCOME files, pull individual and family
information, and display that information in a table.
"""
from prettytable import PrettyTable
from datetime import date
import datetime
import math
import checkErr

## Individual Information Object
class Individual():
    def __init__(self):
        self.id = None
        self.name = None
        self.gender = None
        self.birthday = None
        self.age = None
        self.alive = None
        self.death = None
        self.child = "NA"       # FAMC tag
        self.spouse = "NA "     # FAMS tag
    
    def __iter__(self):
        yield self.id
        yield self.name
        yield self.gender
        yield self.birthday
        yield self.age
        yield self.alive
        yield self.death
        yield self.child
        yield self.spouse

## Family Information Object
class Family():
    def __init__(self):
        self.id = None
        self.married = None
        self.divorced = None
        self.husband = None
        self.husbandName = None
        self.wife = None
        self.wifeName = None
        self.children = []

    def __iter__(self):
        yield self.id
        yield self.married
        yield self.divorced
        yield self.husband
        yield self.husbandName
        yield self.wife
        yield self.wifeName
        yield self.children

## Parse gedcom File - Returns two arrays: Indivduals & Families
def parseFile(data):
    ## Contains Valid Tag and Level Tokens
    valid = {
        0: ["INDI", "FAM", "HEAD", "TRLR", "NOTE"],
        1: ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
        2: "DATE"
    }

    individuals = []
    families = []
    currInd = Individual()
    currFam = Family()
    birthDate = False
    deathDate = False
    marrDate = False
    divDate = False
    space = " "
    lastLine = None

    for line in data:
        inf = line.replace("@", "").strip().split()
        level = int(inf[0])

        ## Check Validity
        levCheck = level in valid
        if levCheck is False:
            tagCheck = False
            continue
        else:
            if len(inf) > 2 and (inf[2] == "INDI" or inf[2] == "FAM"):
                tagCheck = True
            else:
                tagCheck = inf[1] in valid[level]
                if tagCheck == False:
                    continue

        ## Fill In Individual Data
        if (len(inf) > 2) and (inf[2] == "INDI"):
            if (currInd.id == None):
                currInd.id = inf[1]
            else:
                lastLine = inf
                individuals.append(currInd)
                currInd = Individual()
                currInd.id = inf[1]
                continue
        ## Add Name
        if inf[1] == "NAME":
            currInd.name = inf[2] + space + inf[3]     
        ## Add Gender 
        if inf[1] == "SEX":
            currInd.gender = inf[2]                
        if inf[1] == "BIRT":
            birthDate = True
        if inf[1] == "DEAT":
            deathDate = True
        if inf[1] == "DATE":
            ## Adds DOB, ifAlive, and Age
            if birthDate == True:
                strDate = inf[2] + space + inf[3] + space + inf[4]
                date = datetime.datetime.strptime(strDate, "%d %b %Y").date()
                currInd.birthday = date
                currInd.alive = "True"
                birthDate = False

                days_in_year = 365.2425    
                age = int((date.today() - date).days / days_in_year)  # GeeksForGeeks.org
                currInd.age = age
                currInd.death = "NA"
                
            ## Adss DOD, ifAlive, and Age at Death
            elif deathDate == True:
                strDate = inf[2] + space + inf[3] + space + inf[4]
                date = datetime.datetime.strptime(strDate, "%d %b %Y").date()
                currInd.death = date
                currInd.alive = "False"
                deathDate = False
                currInd.age = date.year - currInd.birthday.year
            
            ## Adds Marriage Date to Family
            elif marrDate == True:
                strDate = inf[2] + space + inf[3] + space + inf[4]
                date = datetime.datetime.strptime(strDate, "%d %b %Y").date()
                currFam.married = date
                currFam.divorced = "NA"
                marrDate = False
            
            ## Adds Divorce Date to Family
            elif divDate == True:
                strDate = inf[2] + space + inf[3] + space + inf[4]
                date = datetime.datetime.strptime(strDate, "%d %b %Y").date()
                currFam.divorced = date
                divDate = False

        ## Adds Family Individual is Spouse In
        if inf[1] == "FAMS":
            currInd.spouse = inf[2]
        ## Adds Family Individual is Child In
        if inf[1] == "FAMC":
            currInd.child = inf[2]
        ## Non-Info Lines
        if (inf[1] == "NOTE") or (inf[1] == "HEAD"):
            continue
        ## Fill in  Family Data
        if (len(inf) > 2) and (inf[2] == "FAM"):
            if lastLine[2] == "INDI":
                individuals.append(currInd)
                currInd = Individual()
                lastLine = inf
                currFam.id = inf[1]

            else:
                lastLine = inf
                families.append(currFam)
                currFam = Family()
                currFam.id = inf[1]
                continue

        if inf[1] == "MARR":
            marrDate = True
        if inf[1] == "DIV":
            divDate = True
        ## Add Husband ID
        if inf[1] == "HUSB":
            currFam.husband = inf[2]
            for each in enumerate(individuals):
                if (each[1].id == inf[2]):
                    currFam.husbandName = each[1].name

        ## Add Wife ID
        if inf[1] == "WIFE":
            currFam.wife = inf[2]
            for each in enumerate(individuals):
                if (each[1].id == inf[2]):
                    currFam.wifeName = each[1].name
        ## Add Children in Family to Array
        if inf[1] == "CHIL":
            currFam.children.append(inf[2])
        if inf[1] == "TRLR":
            families.append(currFam)
            currFam = Family()

    return [individuals, families]

## Populates then Prints Indivduals & Families Tables
def createTables(individuals, families):
    indTable = PrettyTable()
    famTable = PrettyTable()
    indTable.field_names = ["ID", "NAME", "GENDER", "BIRTHDAY", "AGE", "ALIVE", "DEATH", "CHILD", "SPOUSE"]
    famTable.field_names = ["ID", "MARRIED", "DIVORCED", "HUSBAND ID", "HUSBAND NAME", "WIFE ID", "WIFE NAME", "CHILDREN"]

    indHold = []
    famHold = []

    ## Individuals Table - Place all info into Nested Array
    for i in enumerate(individuals): 
        indHolder = []
        for each in i[1]:
            indHolder.append(each)
        indHold.append(indHolder)


    ## Populate Individuals Table
    for each in indHold:
        indTable.add_row(each)

    print("Individuals\n", indTable, "\n\n")

    ## Families Table - Place all info into Nested Array
    for j in enumerate(families):
        famHolder = []
        for eachFam in j[1]:
            if eachFam == []:
                eachFam = "NA"
            famHolder.append(eachFam)
        famHold.append(famHolder)
    
    ## Populate Families Table
    for eachh in famHold:
        famTable.add_row(eachh)
    print("Families\n", famTable, "\n\n")

## Check Errors - Acceptance Tests
def checkErrors(individuals, families):
    errLog = []
    
    # Iterate individuals for errors
    count = 0
    for ind in individuals:
        count += 1

         ## US01 - Check All Individuals Dates Before Current Date
        try:
            checkErr.checkCurrDate([], count, errLog, ind)
        except:
            print("checkCurrDate failed1")
        ## US07 - Check Age <150
        try:
            checkErr.checkAge(ind, count, errLog)
        except:
            print("checkAge failed")
        
    # Iterate families for errors
    count = 0
    for fam in families:
        count += 1
        
        ## US01 - Check All Families Dates Before Current Date
        try:
            checkErr.checkCurrDate(fam, count, errLog, [])
        except:
            print("checkCurrDate failed2")
        
        ## US02 - Check Birth Before Marriage
        try:
            checkErr.checkBirth_marriage(fam, count, errLog, individuals)
        except:
            print("checkBirth_marriage failed")
            
        ## US03 - Check Birth before Death
        try:
            checkErr.checkBirth_death(ind, count, errLog)
        except:
            print("checkBirth_death failed")

        ## US04 - Check Marriage before Divorce
        try:
            checkErr.checkMarrBeforeDiv(fam, count, errLog)
        except:
            print("checkMarrBeforeDiv failed")
  
        ## US05 - Check Marriage 
        try:
            checkErr.checkMarriage(fam, count, errLog, individuals)
        except:
            print("checkMarriage Failed")
       
        ## US06 - Check Divorce
        try:
            checkErr.checkDivorce(fam, count, errLog, individuals)
        except:
            print("checkDivorce Failed")
        ## US08 - Check Birth After Parent's Marriage
        try:
            checkErr.checkBirth_parentMarriage(fam, count, errLog, individuals)
        except:
            print("checkBirth_parentMarriage failed")

    return errLog

## Run Program
def run():
    try:
        ## File Name Input and File Open
        # file_name = input("Enter the GEDCOM file path... ")
        # print("Opening "+ file_name + "...\n ")
        # data = open(file_name, 'r')

        # data = open("myFam.ged", 'r')
        data = open("fail.ged", 'r')

        individuals, families = parseFile(data)
        createTables(individuals, families)
        log = checkErrors(individuals, families)

        f = open('Test_Results.txt', 'w')
        for each in log:
            f.write('%s\n' % each)
        f.close()
        
    except:
        print('Unable to open the file...')
        exit()


if __name__ == '__main__':
    run()
