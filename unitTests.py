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
        for fam2 in badFam:
            x = checkErr.checkCurrDate(fam2, 0, [], [])
            self.assertFalse(x)

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
        for fam2 in badFam:
            x = checkErr.checkMarrBeforeDiv(fam2, 0, [])
            self.assertFalse(x)

    ## US05 Test: Marriage before death
    def testMarriage_death_Pass(self):
        for fam2 in goodFam:
            x = checkErr.checkMarriage(fam2, 0, [], goodInd)
            self.assertFalse(x)

    def testMarriage_death_Fail(self):
        res = []
        for fam2 in badFam:
            x = checkErr.checkMarriage(fam2, 0, [], goodInd)
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

    


## Run Unit Tests
if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestAge)
    unittest.TextTestRunner(verbosity = 2).run(suite)