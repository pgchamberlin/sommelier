#!python

from dbconnector import SommelierDbConnector

class Recommender:

    def __init__(self, db=SommelierDbConnector()):
        self.db = db

    def wines_for_wine(self, wine_id):
        return ['wines for wine']

    def wines_for_author(self, author_id):
        return ['wines for author']

