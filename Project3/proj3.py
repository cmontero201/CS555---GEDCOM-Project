"""
Created by Christian Montero
Team Members: Tanmay Bhoir, William DeRoberts, Shoaib Sherwani
September 10, 2019

This file uses python3.6 to parse GEDCOME files, pull individual and family
information, and display that information in a table.

"""
import datetime
import texttable
from datetime import date
import math

## File Name Input and File Open
# file_name = input("Enter the GEDCOM file path... ")
# print("Opening "+ file_name + "...\n ") 
try:
    # data = open(file_name, 'r')
    data = open("myFam.ged", 'r')
except:
    print('Unable to open the file...')
    exit()


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
        self.child = []  # FAMC tag
        self.spouse = []  # FAMS tag


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
    inf = line.strip().split()
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

        ## Adds Divorce Date to Famile
        elif divDate == True:
            strDate = inf[2] + space + inf[3] + space + inf[4]
            date = datetime.datetime.strptime(strDate, "%d %b %Y").date()
            currFam.divorced = date

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

############# CHECKER #############
print("Number of Individuals: ", len(individuals))
table = texttable.Texttable()
headings = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
table.header(headings)

for i in enumerate(individuals):
    row = [i[1].id, i[1].name, i[1].gender, i[1].birthday, i[1].age, i[1].alive, i[1].death,
           str(i[1].child).replace('[', '').replace(']', ''), str(i[1].spouse).replace('[', '').replace(']', '')]
    table.add_row(row)
tab = table.draw()
print(tab)

print("Number of Families: ", len(families))
table2 = texttable.Texttable()
headings2 = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
table2.header(headings2)
for i in enumerate(families):
    row2 = [i[1].id, i[1].married, i[1].divorced, i[1].husband, i[1].husbandName, i[1].wife, i[1].wifeName,
            str(i[1].children).replace('[', '').replace(']', '')]
    table2.add_row(row2)
tab2 = table2.draw()
print(tab2)
