import unittest
import datetime
from datetime import date
from gedcomParser import parseFile, Individual, Family
import checkErr



dataGood = open("myFam.ged", 'r')
dataBad = open("fail.ged", "r")
goodInd, goodFam = parseFile(dataGood)
badInd, badFam = parseFile(dataBad)


## Tests all Age Related User Stories
class TestAge(unittest.TestCase):
    
     ## US01 Test: Dates before Current Date
    def testCurrDate_Pass(self):
        for fam1 in goodFam:
            x = checkErr.checkCurrDate(fam1, 0, [], [])
            self.assertFalse(x)
    def testCurrDate_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkCurrDate(fam2, 0, [], [])
            res.append(x)
        self.assertIn(True, res)

    ## US02 Test: Ensure Birth Date is before Marriage Date
    def testBirth_marriage_Pass(self):
        for fam1 in goodFam:
            x = checkErr.checkBirth_marriage(fam1, 0, [], goodInd)
            self.assertFalse(x)
    def testBirth_marriage_Fail(self):
        res= []
        for fam2 in badFam:
            x = checkErr.checkBirth_marriage(fam2, 0, [], goodInd)
            res.append(x)
        self.assertIn(True, res)
        
    ## US03 Test: Ensure Birth Date is before Death Date
    def testCheckBirth_death_Pass(self):
        for ind1 in goodInd:
            x = checkErr.checkBirth_death(ind1, 0, [])
            if x != None:
                self.assertFalse(x)
    def testCheckBirth_death_Fail(self):
        for ind1 in badInd:
            x = checkErr.checkBirth_death(ind1, 0, [])
            if x != None:
                self.assertTrue(x)
                
    ## US04 Test: Marriage before Divorce
    def testMarriage_Divorce_Pass(self):
        for fam1 in goodFam:
            x = checkErr.checkMarrBeforeDiv(fam1, 0, [])
            self.assertFalse(x)
    def testMarriage_Divorce_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkMarrBeforeDiv(fam2, 0, [])
            res.append(x)
        self.assertIn(True, res)

    ## US05 Test: Marriage before death
    def testMarriage_death_Pass(self):
        res = []
        for fam2 in goodFam:
            x = checkErr.checkMarriage(fam2, 0, [], goodInd)
            self.assertFalse(x)
    def testMarriage_death_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkMarriage(fam2, 0, [], badInd)
            res.append(x)
        self.assertIn(True, res)

    ## US06 Test: Divorce before death
    def testDivorce_death_Pass(self):
        for fam2 in goodFam:
            x = checkErr.checkDivorce(fam2, 0, [], goodInd)
            self.assertFalse(x)
    def testDivorce_death_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkDivorce(fam2, 0, [], goodInd)
            res.append(x)
        self.assertIn(True, res)

    ## US07 Test: Check Age Less Than 150
    def testAge150_Pass(self):
        for ind1 in goodInd:
            x = checkErr.checkAge(ind1, 0, [])
            self.assertFalse(x)
    def testAge150_Fail(self):
        res = []
        for ind2 in badInd:
            x = checkErr.checkAge(ind2, 0, [])
            res.append(x)
        self.assertIn(True, res)
    
    ## US08 Test: Check Birth is after Parent Marriage
    def testBirth_parentMarriage_Pass(self):
        for fam1 in goodFam:
            x = checkErr.checkBirth_parentMarriage(fam1, 0, [], goodInd)
            self.assertFalse(x)
    def testBirth_parentMarriage_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkBirth_parentMarriage(fam2, 0, [], badInd)
            res.append(x)
        self.assertIn(True, res)

    ## US09 Test: Checks Child Birth Before Parent Death (Willy D)
    def testBirthBeforeParentDeath(self):
        testFam = Family()
        testFam.husband = "H1"
        testFam.wife = "W1"
        testFam.children = ["C1"]
        
        husband = Individual()
        husband.id = "H1"
        husband.name = "husband"
        wife = Individual()
        wife.id = "W1"
        wife.name = "wife"
        child = Individual()
        child.id = "C1"
        child.name = "child"
        
        child.birthday = datetime.datetime.strptime("11 nov 1987", "%d %b %Y").date()
        husband.birthday = datetime.datetime.strptime("11 nov 1956", "%d %b %Y").date()
        wife.birthday = datetime.datetime.strptime("11 nov 1956", "%d %b %Y").date()

        #husband/wife alive
        husband.alive = "True"
        wife.alive = "True"
        self.assertFalse(checkErr.checkBirthBeforeParentDeath(testFam, 0, [], [husband, wife, child]))

        #husband/wife died after child born
        husband.alive = "False"
        wife.alive = "False"
        husband.death = datetime.datetime.strptime("12 oct 1990", "%d %b %Y").date()
        wife.death = datetime.datetime.strptime("12 nov 2010", "%d %b %Y").date()
        self.assertFalse(checkErr.checkBirthBeforeParentDeath(testFam, 0, [], [husband, wife, child]))

        #husband/wife died before child born
        husband.death = datetime.datetime.strptime("12 oct 1980", "%d %b %Y").date()
        wife.death = datetime.datetime.strptime("12 oct 1980", "%d %b %Y").date()
        self.assertTrue(checkErr.checkBirthBeforeParentDeath(testFam, 0, [], [husband, wife, child]))

        #husband/wife died day child born
        husband.death = child.birthday
        wife.death = child.birthday
        self.assertFalse(checkErr.checkBirthBeforeParentDeath(testFam, 0, [], [husband, wife, child]))

    ## US10 Test: Marriage before 14
    def testMarrBefore14_Pass(self):
        for fam1 in goodFam:
            x=checkErr.checkMarrAfter14(goodInd, fam1, 0, [])
            self.assertFalse(x)
    def testMarrBefore14_Fail(self):
        res=[]
        for fam2 in badFam:
            x=checkErr.checkMarrAfter14(badInd, fam2, 0, [])
            res.append(x)
        self.assertIn(True, res)
        
    ## US11 Test: Checks Divorce Before Re-Marriage (Willy D)
    def testDivorceBeforeRemarriage(self):
        testFam1 = Family()
        testFam1.id = "F1"
        testFam1.husband = "H1"
        testFam1.husbandName = "Husband1"
        testFam1.wife = "Wife1"
        testFam1.wifeName = "Wife1"
        testFam1.married = datetime.datetime.strptime("12 oct 1980", "%d %b %Y").date()
        testFam1.divorced = datetime.datetime.strptime("12 oct 2000", "%d %b %Y").date()
        
        testFam2 = Family()
        testFam2.id = "F2"
        testFam2.husband = "H1"
        testFam2.husbandName = "Husband1"
        testFam2.wife = "W2"
        testFam2.wifeName = "wife2"
        testFam2.married = datetime.datetime.strptime("12 oct 2010", "%d %b %Y").date()
        testFam2.divorced = "NA"

        self.assertFalse(checkErr.checkDivorcebeforeRemarriage(testFam1, 0, [], [testFam1, testFam2]))

        testFam2.married = datetime.datetime.strptime("12 oct 1999", "%d %b %Y").date()
        self.assertTrue(checkErr.checkDivorcebeforeRemarriage(testFam1, 0, [], [testFam1, testFam2]))

        testFam2.married = testFam1.divorced
        self.assertFalse(checkErr.checkDivorcebeforeRemarriage(testFam1, 0, [], [testFam1, testFam2]))

    ## US12 Test: Check Marriage Age
    def testMarriageAge_Pass(self):
        for fam1 in goodFam:
            x=checkErr.marriage_age(fam1, 0, [], goodInd)
            self.assertFalse(x)

    def testMarriageAge_Fail(self):
        res=[]
        for fam2 in badFam:
            x=checkErr.marriage_age(fam2, 0, [], badInd)
            res.append(x)
        self.assertIn(True, res)

    ## US13 Test: Check Sibling Spaces
    def testSiblingSpaces_Pass(self):
        for fam1 in goodFam:
            x = checkErr.siblingspaces(fam1, 0, [], goodInd)
            self.assertFalse(x)

    def testSiblingSpaces_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.siblingspaces(fam2, 0, [], badInd)
            res.append(x)
        self.assertIn(True, res)

    ## US14 Test: Check Multiple Births Less Than 6
    def testMultipleBirths_Pass(self):
        for fam1 in goodFam:
            x = checkErr.checkMultipleBirths(fam1, 0, [], goodInd)
            self.assertFalse(x)
    def testMultipleBirths_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkMultipleBirths(fam2, 0, [], badInd)
            res.append(x)
        self.assertIn(True, res)

    ## US15 Test: Check Family Has Less Than 16 Children
    def testSiblingCount_Pass(self):
        for fam1 in goodFam:
            x = checkErr.checkSiblingCount(fam1, 0, [])
            self.assertFalse(x)
    def testSiblingCount_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkSiblingCount(fam2, 0, [])
            res.append(x)
        self.assertIn(True, res)

    ## US16 Male Last Names Checks
    def testLastNames_Pass(self):
        for fam1 in goodFam:
            x=checkErr.male_last_name(fam1, 0, [], goodInd)
            self.assertFalse(x)
    def testLastNames_Fail(self):
        res=[]
        for fam2 in badFam:
            x=checkErr.male_last_name(fam2, 0, [], badInd)
            res.append(x)
        self.assertIn(True, res)
    
    ## US23 Duplicate Names and Birthdays
    def testDuplicate_names_birthdays_Pass(self):
        for ind1 in goodInd:
            x = checkErr.check_duplicate_names_birthdays(ind1, goodInd, 0, [])
            self.assertFalse(x)
    def testDuplicate_names_birthdays_Fail(self):
        res = []
        for ind2 in badInd:
            x = checkErr.check_duplicate_names_birthdays(ind2, badInd, 0, [])
            res.append(x)
        self.assertIn(True, res)

    ## US24 Multi-Family Parents
    def testMulti_family_parent_Pass(self):
        for fam1 in goodFam:
            x = checkErr.check_multi_family_parent(fam1, 0, [], goodFam)
            print(x)
            self.assertFalse(x)
    def testMulti_family_parent_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.check_multi_family_parent(fam2, 0, [], badFam)
            res.append(x)
        self.assertIn(True, res)


## Run Unit Tests
if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestAge)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    
