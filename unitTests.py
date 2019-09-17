import unittest
import datetime
from datetime import date
from gedcomParser import parseFile, Individual, Family
import checkErr


# goodInd = Individual()
goodInd = Individual()
goodInd.id = "Test00"
goodInd.name = "TEST /PERSON/"
goodInd.gender = "M"
goodInd.birthday = datetime.datetime.strptime("9 NOV 2007", "%d %b %Y").date()
goodInd.age = 65
goodInd.alive = True
# goodFam = 
badInd = Individual()
badInd.id = "Test00"
badInd.name = "TEST /PERSON/"
badInd.gender = "M"
badInd.birthday = datetime.datetime.strptime("9 NOV 2020", "%d %b %Y").date()
badInd.age = 162
badInd.alive = True






## Tests all Age Related User Stories
class TestAge(unittest.TestCase):

    ## US07 Test: Check Age Less Than 150
    def testAge150_Pass(self):
        x = checkErr.checkAge(goodInd, 0, [])
        self.assertFalse(checkErr.checkAge(goodInd, 0, []))
    def testAge150_Fail(self):
        x = checkErr.checkAge(badInd, 0, [])
        self.assertTrue(checkErr.checkAge(badInd, 0, []))

    ## US08 Test: Ensure Birth Date is before Marriage Date


## Run Unit Tests
if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestAge)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    