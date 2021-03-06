from datetime import date, timedelta
from stockInfo import stockInfo
from stockAnalysis import *
from stockUtil import *
import unittest

class testStockInfo(unittest.TestCase):
    
    def setUp(self):
        self.testobj = stockInfo("MSFT")

    #Test whether it is a correct object
    def test_creation(self):
        self.assertEqual(self.testobj.ticker, "MSFT")
        
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

        h = self.testobj.listFromTo(date(2009,2,2),date(2009,3,2))
        l= map( (lambda l: l[6]), self.testobj.listFromTo(date(2008,1,2),date(2009,3,2)))
        r = []
        for i in range(len(l)-20):
            r.append(sum(l[i:i+20])/20)
        k = movingAverage(self.testobj,20,date(2009,2,2),date(2009,3,2))
        r = r[-len(k):] 
        self.assertEqual(len(h),len(k))
        self.assertListEqual(r,k)


    #Check if it fails for invalid dates, and works for valid
    def test_Beta(self):
        with self.assertRaises(ValueError):
            Beta(self.testobj,date.min)
        self.assertIsInstance(Beta(self.testobj),float)
        SP500 = stockInfo("^GSPC")
        self.assertEqual(Beta(SP500),1)
            
    #Check as much as we can of RSS
    def test_Rss(self):
        self.assertIsInstance(self.testobj.getRSS(),list)
    
    #check BuyOrSell
    def test_BuyOrSell(self):
        k = movingAverage(self.testobj,50).pop()
        j = movingAverage(self.testobj,200).pop()
        if k > j:
            t = 1
        else:
            if k < j:
                t = -1
        self.assertEqual(BuyOrSell(self.testobj),t)


    #Check as we can of getCurrent
    def test_current(self):
        self.assertIsInstance(self.testobj.getCurrent(),dict)
        
    #Test  getDate by comparing to easily retrievable value
    def test_getDate(self):
        self.assertEqual(self.testobj.getDate(self.testobj.fromDate)["Open"],self.testobj.infoList[0][1])
                         
if __name__== '__main__':
    unittest.main(verbosity=2, exit=False)
