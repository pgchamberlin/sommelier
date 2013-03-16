#!python
from sommelier import SommelierDb, SommelierBroker
import math

class UserBroker(SommelierBroker):

    usersquery = "SELECT * FROM sommelier_user LIMIT {} OFFSET {}";
    userquery  = "SELECT * FROM sommelier_user WHERE id = {}";
    countquery = "SELECT COUNT(*) FROM sommelier_user"
    pagesize = 50

    def __init__(self, db=SommelierDb()):
        self.db = db

    def getPage(self, pagenum=1):
        pageparams = self.pagesize, self.pagesize * (pagenum - 1)
        self.db.execute(self.usersquery.format(*pageparams))
        return self.db.fetchall()

    def getNumPages(self):
        self.db.execute(self.countquery)
        result = self.db.fetchone()
        count = float( result['COUNT(*)'] );
        return int( math.ceil( count / self.pagesize ) )

    def getUser(self, userid):
        self.db.execute(self.userquery.format(userid))
        return self.db.fetchone()
