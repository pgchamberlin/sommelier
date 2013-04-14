#!python

import os
import collections
import json

from brokers import SommelierBroker

class Recommender:

    sparse_ui_matrix_filename = 'ui_matrix_sparse.json'

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    def wines_for_wine(self, wine_id):
        return ['wines for wine']

    def wines_for_author(self, author_id):
        return ['wines for author']

    # generate the sparse ui matrix and save it to disk
    def create_sparse_ui_matrix(self):
        matrix = self.generate_sparse_ui_matrix()
        self.save_json_file(self.sparse_ui_matrix_filename, matrix)

    # load the sparse ui matrix from disk
    def load_sparse_ui_matrix(self):
        return self.load_json_file(self.sparse_ui_matrix_filename)

    # generates the spares user-item matrix for authors and wines
    def generate_sparse_ui_matrix(self):

        # get all the tastings from the database
        tastings = self.broker.get_rating_data()

        # make a dict with an entry for each author, with wines and ratings:
        # { author: { wine_id: rating, wine_id: rating, ... } ... }
        author_ratings = {}
        for tasting in tastings:
            author_ratings.setdefault(tasting['author_id'], {})
            author_ratings[tasting['author_id']][tasting['wine_id']] = tasting['rating']

        # now get all the wine ids
        wines = self.broker.get_wine_ids()

        # for each author iterate over wines and make a tuple with ratings for each wine, or 0.0
        sparse_matrix = []
        for item in author_ratings:
            author = author_ratings[item]
            author_vector = []
            for wine in wines:
                # if there is a key in the author dict for this wine, take the rating from that
                if wine['id'] in author:
                    author_vector.append(float(author[wine['id']]))
                # otherwise append a 0.0
                else:
                    author_vector.append(0.0)
            sparse_matrix.append(author_vector)
        return sparse_matrix

    def get_data_file_dir_path(self):
        return "".join([os.getcwd(), '/data/'])

    def save_json_file(self, filename, data):
        thefile = "".join([self.get_data_file_dir_path(), filename])
        with open(thefile, 'w') as outfile:
            json.dump(data, outfile)

    def load_json_file(self, filename):
        return json.loads(open("".join([self.get_data_file_dir_path(), filename])).read())

