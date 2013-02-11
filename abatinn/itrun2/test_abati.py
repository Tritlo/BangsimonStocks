from datetime import date, timedelta
from stockInfo import stockInfo
from stockAnalysis import *
from stockUtil import *
import unittest

class testStockInfo(unittest.TestCase):
    
    def setUp(self):
        self.testobj = stockInfo("GOOG")

    #Test whether it is a correct object
    def test_creation(self):
        self.assertEqual(self.testobj.ticker, "GOOG")
        
    #Make sure it returns an error on an invalid object
    def test_invalidcreation(self):
        with self.assertRaises(ValueError):
            otherobj = stockInfo("ThingThatDoesNotExist")

    #Test that dates are within a valid range and not haywire
    def test_dates(self):
        self.assertGreaterEqual(self.testobj.fromDate,date.min)
        self.assertLessEqual(self.testobj.toDate,date.today())

    #Test whether we have any information
    def test_inform(self):
        self.assertIsNot(self.testobj.infoList, [])

    #Check if validdates works
    def test_validdate(self):
        days = timedelta(10)
        self.assertFalse(self.testobj.validDate(self.testobj.toDate+days))
        self.assertTrue(self.testobj.validDate(self.testobj.toDate-days))

    #Check if listFromTo works correctly
    def test_listfromTo(self):
        self.assertListEqual(self.testobj.infoList,self.testobj.listFromTo(self.testobj.fromDate,self.testobj.toDate))

    #Check if stringToDate in stockUtil works correctly
    def test_stringToDate(self):
        self.assertEqual(stringToDate("2004-04-01"),date(2004,04,01))

    #Check if dateToString in stockUtil works correctly
    def test_dateToString(self):
        self.assertEqual("2004-04-01",dateToString(date(2004,04,01)))

    #Check if movingAverage works correctly in base case, and is invalid for invalid dates
    def test_movingAvg(self):
        adjCloses = []
        for i in self.testobj.infoList:
            adjCloses.append(i[6])
        self.assertListEqual(movingAverage(self.testobj, 1),adjCloses)
        with self.assertRaises(ValueError):
            movingAverage(self.testobj,2,date.min)

    #Check if it fails for invalid dates, and works for valid
    def test_Beta(self):
        with self.assertRaises(ValueError):
            Beta(self.testobj,date.min)
        self.assertIsInstance(Beta(self.testobj),float)
        
    #Check as much as we can of RSS
    def test_Rss(self):
        self.assertIsInstance(self.testobj.getRSS(),list)

    #Check as we can of getCurrent
    def test_current(self):
        self.assertIsInstance(self.testobj.getCurrent(),dict)
        
    #Test  getDate by comparing to easily retrievable value
    def test_getDate(self):
        self.assertEqual(self.testobj.getDate(self.testobj.fromDate)["Open"],self.testobj.infoList[0][1])
                         
if __name__== '__main__':
    unittest.main(verbosity=2, exit=False)
