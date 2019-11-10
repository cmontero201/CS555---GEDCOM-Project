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
        self.child = "NA"  # FAMC tag
        self.spouse = "NA "  # FAMS tag

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


def getIndividual(personID: object, individuals: object) -> object:
    for i in individuals:
        if personID == i.id:
            return i
    return False


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


# US28 Sorts a list of IDs by age from greatest to smallest
def sortByAge(indList, individuals):
    children = {}
    for i in indList:
        child = getIndividual(i, individuals)
        if child is not False: #if child exists
            if child.age is not None:
                children[i] = child.age
            else:
                children[i] = -1

    sortedChildren = []
    for c in sorted(children.items(), key = lambda age: age[1], reverse = True):
        sortedChildren.append(c[0])

    return sortedChildren

# US32 Check multiple births
def getBirthCount(individuals, family):
    birthcount = {}

    for c in family.children:
        birthday = getIndividual(c, individuals).birthday
        #print(birthday)
        if birthday in birthcount:
            birthcount[birthday].append(c)
        else:
            birthcount[birthday] = [c]

    return birthcount


## US31 List all living people over 30 who have never been married 
def livingInd(individuals, families):
    people = []

    for ind in individuals:
        ind_id = ind.id

        for fam in families:
            husband = fam.husband
            wife = fam.wife

            if (ind_id != husband) and (ind_id != wife) and (ind.age >= 30) and (ind.alive == "True"):
                people.append(ind)
            else:
                continue
    
    x = people
    people = []

    for each in x:
        if each not in people:
            people.append(each)
    return people

## US33 Finds Children under 18 with Deceased Parents
def isOrphan(person, individuals, families):
    if person.age is not None:
        if person.age < 18:
            parents = checkErr.getParents(person.id, families)
            if len(parents) > 0:
                parent1, parent2 = parents[0], parents[1]
                if (getIndividual(parent1, individuals).death != "NA") and (
                        getIndividual(parent2, individuals).death != "NA"):
                    return True
            else:
                return False

    return False

## US38 Finds Individuals with Birthdays in the next 30 Days
def getUpcomingBirthdays(individuals):
    curr_date = date.today()
    month_window = curr_date + datetime.timedelta(days=30)
    upcoming = []

    for ind in individuals:
        birthday = ind.birthday
        comp = datetime.date(curr_date.year, birthday.month, birthday.day)
        delta = (comp - curr_date).days

        if (delta > 0) and (delta <= 30) and (ind.alive == "True"):
            upcoming.append(ind)

    return upcoming


## Populates then Prints Indivduals & Families Tables
def createTables(individuals, families):
    indTable = PrettyTable()
    famTable = PrettyTable()
    orphanTable = PrettyTable()
    birthdayTable = PrettyTable()
    deceasedTable = PrettyTable()
    married_livingTable = PrettyTable()
    livingindTable = PrettyTable()
    multipleBirthTable = PrettyTable()
    indTable.field_names = ["ID", "NAME", "GENDER", "BIRTHDAY", "AGE", "ALIVE", "DEATH", "CHILD", "SPOUSE"]
    famTable.field_names = ["ID", "MARRIED", "DIVORCED", "HUSBAND ID", "HUSBAND NAME", "WIFE ID", "WIFE NAME",
                            "CHILDREN"]
    orphanTable.field_names = ["ID", "NAME", "AGE"]
    birthdayTable.field_names = ["ID", "NAME", "BIRTHDAY", "AGE"]
    deceasedTable.field_names = ["ID","NAME", "AGE", "DEATH DATE"]
    married_livingTable.field_names = ["FAM ID", "HUSBAND NAME", "WIFE NAME","MARIAGE DATE", "ALIVE HUSBAND", "ALIVE WIFE"]
    livingindTable.field_names = ["ID", "NAME", "GENDER", "AGE"]
    multipleBirthTable.field_names = ["FAM ID", "BIRTHDATE", "CHILDREN"]

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
        j[1].children = sortByAge(j[1].children, individuals)
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

    # Multiple Births table
    # US 32 - Print multiple births
    for f in families:
        print(getBirthCount(individuals, f))
        for b in getBirthCount(individuals, f):
            multipleBirthTable.add_row([f.id, b[0], b[1]])
    print("Multiple Births\n", multipleBirthTable, "\n\n")

    ## Orphan Table 
    ## US 33 - Print orphans
    for i in individuals:
        if isOrphan(i, individuals, families):
            orphanTable.add_row([i.id, i.name, i.age])
    print("Orphans\n", orphanTable, "\n\n")

    ## Deceased Table
    ## US29 - Print Deceased Individuals
    for i in individuals:
        if i.alive != 'True':
            deceasedTable.add_row([i.id, i.name, i.age, i.death])
    print("Deceased Individuals\n", deceasedTable, "\n\n")

    ## US30 Living and Married
    for fam in families:
        if fam.married is not None:
            husband_alive, wife_alive= checkErr.check_isalive(fam.husbandName, fam.wifeName, individuals)
            if husband_alive == True and wife_alive == True:
                married_livingTable.add_row(
                    [fam.id, fam.husbandName, fam.wifeName, fam.married, husband_alive, wife_alive])
    print("Married and Living \n", married_livingTable, "\n\n")

    ## US31 - Print living individuals over 30 and unmarried
    living_individuals = livingInd(individuals, families)
    for i in living_individuals:
        livingindTable.add_row([i.id, i.name, i.gender, i.age])
    print("Living Individuals Over 30 & Unmarried\n", livingindTable, "\n\n")

    ## US 38 - Upcoming Birthdays Table
    bdays = getUpcomingBirthdays(individuals)
    for i in bdays:
        birthdayTable.add_row([i.id, i.name, i.birthday, i.age])
    print("\U0001F382  Upcoming Birthdays \U0001F382\n", birthdayTable, "\n\n")

    return (indTable, famTable, orphanTable, birthdayTable, married_livingTable, deceasedTable, livingindTable)



## Check Errors - Acceptance Tests
def checkErrors(individuals, families):
    errLog = []

    # US22 Unique ID
    try:
        checkErr.unique_id_check(families, errLog, individuals)
    except:
        print("Unique ID failed")

    # Iterate individuals for errors
    count = 0
    for ind in individuals:
        count += 1

        ## US01 - Check All Individuals Dates Before Current Date
        try:
            checkErr.checkCurrDate([], count, errLog, ind)
        except:
            print("checkCurrDate failed1")
        ## US03 - Check Birth before Death
        try:
            checkErr.checkBirth_death(ind, count, errLog)
        except:
            print("checkBirth_death failed")
        ## US07 - Check Age <150
        try:
            checkErr.checkAge(ind, count, errLog)
        except:
            print("checkAge failed")
        ## US23 - Check Unique Name & Birthday Combo
        try:
            checkErr.check_duplicate_names_birthdays(ind, individuals, count, errLog)
        except:
            print("check_duplicate_names_birthdays failed")

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
        ## US09 - Check Birth Before Paren't Death
        try:
            checkErr.checkBirthBeforeParentDeath(fam, count, errLog, individuals)
        except:
            print("checkBirthBeforeParentDeath failed")
        ## US10 - Check parents are atleast 14 years old 
        try:
            checkErr.checkMarrAfter14(individuals, fam, count, errLog)
        except:
            print("checkMarrAfter14 failed")
        ## US11 - Check Divorce occurs before re-marriage
        try:
            checkErr.checkDivorcebeforeRemarriage(fam, count, errLog, families)
        except:
            print("checkDivorcebeforeRemarriage failed")
        ## US12 - Marriage Age
        try:
            checkErr.marriage_age(fam, count, errLog, individuals)
        except Exception as ex:
            print("Marriage Age failed")
        ## US13 - Sibling Spaces
        try:
            checkErr.siblingspaces(fam, count, errLog, individuals)
        except Exception as ex:
            print("Sibling Spaces failed")
        ## US14 - Multiple Births Less Than 6
        try:
            checkErr.checkMultipleBirths(fam, count, errLog, individuals)
        except:
            print("checkMultipleBirths failed")
        ## US15 - Check Family Has Less Than 16 Children
        try:
            checkErr.checkSiblingCount(fam, count, errLog)
        except:
            print("checkSiblingCount failed")
        ## US16 - Male last names
        try:
            checkErr.male_last_name(fam, count, errLog, individuals)
        except Exception as ex:
            print("Sibling Spaces failed")
        ## US17 - Parents should not marry their children
        try:
            checkErr.checkNoMarrChild(fam, count, errLog, families)
        except:
            print("checkNoMarrChild failed")
            ## US18 - Siblings should not marry
        try:
            checkErr.checkNoSiblingsMarry(fam, count, errLog, families)
        except:
            print("checkNoSiblingsMarry failed")
        ## US19 - Check is cousins are married
        try:
            checkErr.checkCousinsMarried(fam, count, errLog, families)
        except:
            print("checkCousinsMarried failed")
        ## US20 - Check is a person is married to their aunt or uncle
        try:
            checkErr.checkMarriedtoAuntUncle(fam, count, errLog, families)
        except:
            print("checkMarriedtoAuntUncle failed")

        ## US21 - Correct gender for role
        try:
            checkErr.gender_role_check(fam, count, errLog, individuals)
        except Exception as ex:
            print("Gender Role Check failed")

        ## US24 - Multi-Family Parents
        try:
            checkErr.check_multi_family_parent(fam, count, errLog, families)
        except:
            print("check_multi_family_parent failed")

        ## US25 - Check Unique Names & DOB in Families
        try:
            checkErr.check_unique_family_names_dob(fam, count, errLog, individuals)
        except:
            print("check_unique_family_names_dob failed")

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

        ind_table, fam_table, orph_table, birthday_table, married_livingTable, deceasedTable, living_ind_table = createTables(individuals, families)

        log = checkErrors(individuals, families)

        f = open('Test_Results.txt', 'w')
        f.write("Individuals\n")
        f.write(ind_table.get_string())
        f.write("\n\nFamilies\n")
        f.write(fam_table.get_string())
        f.write("\n\n\U0001F382 Upcoming Birthdays \U0001F382\n")
        f.write(birthday_table.get_string())
        f.write("\n\nMarried and Living\n")
        f.write(married_livingTable.get_string())
        f.write("\n\n Living Individuals over 30 & unmarried \n")
        f.write(living_ind_table.get_string())
        f.write("\n\nDeceased Individuals\n")
        f.write(deceasedTable.get_string())
        f.write("\n\nChildren with Deceased Parents\n")
        f.write(orph_table.get_string())
        f.write("\n\n************************************************* \n\t\t\t\tERROR LOG\n*************************************************\n")
        for each in log:
            f.write('%s\n' % each)
        f.close()

        return (individuals, families, log)
    except:
        print('Unable to open the file...')
        exit()


if __name__ == '__main__':
    run()
