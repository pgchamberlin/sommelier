#!python
from sommelier import sommelierdb
import math

class WineBroker:

  winesquery = "SELECT * FROM sommelier LIMIT {} OFFSET {}";
  countquery = "SELECT COUNT(*) FROM sommelier"
  pagesize = 50
  db = sommelierdb.SommelierDb()

  def getPage(self, pagenum=1):
    pageparams = self.pagesize, self.pagesize * (pagenum - 1)
    self.db.execute(self.winesquery.format(*pageparams))
    return self.db.fetchall()

  def getNumPages(self):
    self.db.execute(self.countquery)
    result = self.db.fetchone()
    count = float( result['COUNT(*)'] );
    return int( math.ceil( count / self.pagesize ) )

