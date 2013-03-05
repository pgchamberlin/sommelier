#!python

import MySQLdb
from MySQLdb.constants import FIELD_TYPE
from MySQLdb.cursors import DictCursor

class SommelierDb:
  
  cursor = None
  connection = None

  def __init__(self):
    converter = { FIELD_TYPE.LONG: int }
    self.connection = MySQLdb.connect(user="sommelier",db="sommelier",passwd="vinorosso",conv=converter)
    self.connection.set_character_set('utf8')
    self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
    self.cursor.execute('SET NAMES utf8;')
    self.cursor.execute('SET CHARACTER SET utf8;')
    self.cursor.execute('SET character_set_connection=utf8;')

  def execute(self, query):
    return self.cursor.execute(query)

  def fetchone(self):
    return self.cursor.fetchone()

  def fetchall(self):
    return self.cursor.fetchall()

  def __del__(self):
    if self.cursor is not None:
      self.cursor.close()
    if self.connection is not None:
      self.connection.close()

