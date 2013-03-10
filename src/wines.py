#!python
from sommelierdb import SommelierDb
import math

class WineBroker:

    winesquery = "SELECT * FROM sommelier LIMIT {} OFFSET {}";
    winequery  = "SELECT * FROM sommelier WHERE id = {}";
    countquery = "SELECT COUNT(*) FROM sommelier"
    pagesize = 50

    def __init__(self, db=SommelierDb()):
        self.db = db

    def getPage(self, pagenum=1):
        pageparams = self.pagesize, self.pagesize * (pagenum - 1)
        self.db.execute(self.winesquery.format(*pageparams))
        return self.db.fetchall()

    def getNumPages(self):
        self.db.execute(self.countquery)
        result = self.db.fetchone()
        count = float( result['COUNT(*)'] );
        return int( math.ceil( count / self.pagesize ) )

    def getWine(self, wineid):
        self.db.execute(self.winequery.format(wineid))
        return self.db.fetchone()

