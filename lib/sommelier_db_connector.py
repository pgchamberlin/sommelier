# a db connector for accessing the wine dev database
# DB Credentials
# 'sommelier'@'localhost' IDENTIFIED BY 'vinorosso';

import MySQLdb

class SommelierDbConnector:

  def __init__(self):
    self.db=MySQLdb.connect(host='localhost',name='sommelier',passwd='vinorosso',db='wine')


