#!python
import unittest
import pprint
from mock import Mock, MagicMock
from wines import WineBroker

class WinesTest(unittest.TestCase):

    def setUp(self):
        dbmock = {}
        self.winebroker = WineBroker()
        self.winebroker.db.execute = MagicMock()
        self.winebroker.db.fetchall = MagicMock()
    
    def testGetPage(self):
        page = self.winebroker.getPage(1)
        expectedquery = "SELECT * FROM sommelier LIMIT 50 OFFSET 0"
        self.winebroker.db.execute.assert_called_once_with(expectedquery)
        self.winebroker.db.fetchall.assert_called_once()
    
    def testGetNumPages(self):
        numpages = self.winebroker.getNumPages()
        expectedquery = "SELECT COUNT(*) FROM sommelier"
        self.winebroker.db.execute.assert_called_once_with(expectedquery)
        self.winebroker.db.fetchone.assert_called_once()
    
    def testGetWine(self):
        wine = self.winebroker.getWine(123)
        expectedquery = "SELECT * FROM sommelier WHERE id = 123"
        self.winebroker.db.execute.assert_called_once_with(expectedquery)
        self.winebroker.db.fetchone.assert_called_once()

if __name__ == '__main__':
    unittest.main()

