from datetime import date
from stockInfo import stockInfo
from stockAnalysis import *
import unittest

class testStockInfo(unittest.TestCase):
    def setUp(self):
        self.testobj = stockInfo("GOOG")
        
    #Gaum hvort thad verdi til
    def test_creation(self):
        self.assertEqual(self.testobj.ticker, "GOOG")
        
    #Gaum hvort thad gefi ekki villu vid vitlausan hlut
    def test_invalidcreation(self):
        with self.assertRaises(ValueError):
            otherobj = stockInfo("ThingThatDoesNotExist")

    #Athugum hvort dagsetningar seu ekki rettar
    def test_dates(self):
        self.assertGreaterEqual(self.testobj.fromDate,date.min)
        self.assertLessEqual(self.testobj.toDate,date.today())

    #Athugum hvort ad vid seum ekki med einhverjar upplysingar
    def test_inform(self):
        self.assertIsNot(self.testobj.infoList, [])

if __name__== '__main__':
    unittest.main(verbosity=2, exit=False)
