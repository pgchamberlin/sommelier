#!python

import os
import collections
import json

import numpy
from numpy import random

from brokers import SommelierBroker

class Recommender:

    lists_ui_matrix_filename = 'ui_matrix_lists.json'
    factored_ui_matrix_filename = 'ui_matrix_lists_factored.json'
    tastings_movielens_format_filename = 'tastings_movielends_format.dat'
    tastings_recsys_svd_filename = 'recsys_svd_data.dat'

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    def wines_for_wine(self, wine_id):
        svd = self.load_recsys_svd(k=100, min_values=3, verbose=False)

        # there may not be recommendations for this author, which would
        # raise a KeyError. We don't want a KeyError, an empty list is fine!
        try:
            # get similar wines, but pop() the first item off as it is the current wine
            recommendations = svd.similar(int(wine_id.encode('ascii')))
            recommendations.pop(0)
        except:
            recommendations = []

        wine_ids = []
        for recommendation in recommendations:
            wine_ids.append(recommendation[0])

        similar_wines = []
        if len(wine_ids) > 0:
            wines = self.broker.get_wines_by_id(wine_ids)
            for wine in wines:
                similar_wines.append({
                    'name': wine['name'],
                    'vintage': wine['vintage'],
                    'id': wine['id']
                })

        return similar_wines

    def wines_for_author(self, author_id):
        svd = self.load_recsys_svd(k=100, min_values=3, verbose=False)

        # there may not be recommendations for this author, which would
        # raise a KeyError. We don't want a KeyError, an empty list is fine!
        try:
            recommendations = svd.recommend(int(author_id.encode('ascii')), is_row=False)
        except:
            recommendations = []

        wine_ids = []
        for recommendation in recommendations:
            wine_ids.append(recommendation[0])

        recommended_wines = []
        if len(wine_ids) > 0:
            wines = self.broker.get_wines_by_id(wine_ids)
            for wine in wines:
                recommended_wines.append({
                    'name': wine['name'],
                    'vintage': wine['vintage'],
                    'id': wine['id']
                })
        
        return recommended_wines

    # generate the sparse ui matrix and save it to disk
    def create_lists_ui_matrix(self):
        matrix = self.generate_lists_ui_matrix()
        self.save_json_file(self.lists_ui_matrix_filename, matrix)

    # load the sparse ui matrix from disk
    def load_lists_ui_matrix(self):
        return self.load_json_file(self.lists_ui_matrix_filename)

    # generates the sparse user-item matrix for authors and wines
    def generate_sparse_ui_matrix(self):
        return []

    def generate_lists_ui_matrix(self):
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
        lists_matrix = []
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
            lists_matrix.append(author_vector)
        return lists_matrix

    def data_file_directory(self):
        return "".join([os.getcwd(), '/data/'])

    def file_location(self, filename):
        return "".join([self.data_file_directory(), filename])

    def save_json_file(self, filename, data):
        thefile = "".join([self.data_file_directory(), filename])
        with open(thefile, 'w') as outfile:
            json.dump(data, outfile)

    def load_json_file(self, filename):
        print "".join(["Loading ", self.data_file_directory(), filename])
        return json.loads(open("".join([self.data_file_directory(), filename])).read())

    # Copied from Albert Yeung: http://www.quuxlabs.com/wp-content/uploads/2010/09/mf.py_.txt
    def factor_lists_ui_matrix(self, steps=5000):
        print "Loading sparse matrix..."
        R = self.load_lists_ui_matrix()
        print "Done."
        #R = [
        #    [5,3,0,1],
        #    [4,0,0,1],
        #    [1,1,0,5],
        #    [1,0,0,4],
        #    [0,1,5,4],
        #]

        print "Converting to numpy.array()..."
        R = numpy.array(R)
        print "Done."
        N = len(R)
        M = len(R[0])
        K = 2

        print "Creating random matrices..."
        P = numpy.random.rand(N, K)
        Q = numpy.random.rand(M, K)
        print "Done."

        print "Beginning matrix factorization..."
        nP, nQ = self.matrix_factorization(R, P, Q, K, steps)
        print "Done."

        print "Dotting generated matrices..."
        nR = numpy.dot(nP, nQ.T)
        print "Done."

        print "Saving to JSON file..."
        self.save_json_file("".join([self.factored_ui_matrix_filename, str(steps)]), nR.tolist())
        print "Done."

        return nR

    # Copied from Albert Yeung: http://www.quuxlabs.com/wp-content/uploads/2010/09/mf.py_.txt
    def matrix_factorization(self, R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
        print "".join(["Matrix Factorization"])
        print "".join(["Steps: ", str(steps)])
        Q = Q.T
        s = 0
        for step in xrange(steps):
            s+=1
            print "Step %d / %d" % (s,steps)
        
            for i in xrange(len(R)):
                for j in xrange(len(R[i])):
                    if R[i][j] > 0:
                        eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                        for k in xrange(K):
                            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
            eR = numpy.dot(P,Q)
            e = 0
            for i in xrange(len(R)):
                for j in xrange(len(R[i])):
                    if R[i][j] > 0:
                        e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                        for k in xrange(K):
                            e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
            if e < 0.001:
                break
        return P, Q.T

    def save_sommelier_tastings_to_movielens_format_file(self):
        tastings = self.broker.get_rating_data()

        # make a list of strings which will be the lines in our 
        # Movielens format data file. The format is:
        # AuthorId::WineId::Rating::Timestamp
        import time
        outfile = self.file_location(self.tastings_movielens_format_filename)
        with open(outfile, 'w') as datafile:
            for tasting in tastings:
                # if the date is not valid set to 0, otherwise convert to Unix epoch
                date = '0'
                if tasting['tasting_date'] != '0000-00-00 00:00:00':
                    date = str(time.mktime(time.strptime(tasting['tasting_date'], "%Y-%m-%d %H:%M:%S"))).encode('utf-8')
                row = "".join([
                    str(tasting['author_id']).encode('utf-8'), '::', 
                    str(tasting['wine_id']).encode('utf-8'), '::', 
                    str(float(tasting['rating'])).encode('utf-8'), '::', 
                    date, '\n'])
                datafile.write(row)

    # loads source_file (Movielens format) and performs SVD
    # saving 
    def create_tastings_recsys_svd_data(self, k=100, min_values=2, verbose=True):
        
        # create a data file in Movielens format with the tastings data
        self.save_sommelier_tastings_to_movielens_format_file()

        import recsys.algorithm
        if verbose:
            recsys.algorithm.VERBOSE = True

        from recsys.algorithm.factorize import SVD
        svd = SVD()

        # load source data, perform SVD, save to zip file
        source_file = self.file_location(self.tastings_movielens_format_filename)
        svd.load_data(filename=source_file, sep='::', format={'col':0, 'row':1, 'value':2, 'ids': int})

        outfile = self.file_location(self.tastings_recsys_svd_filename)
        svd.compute(k=k, min_values=min_values, pre_normalize=None, mean_center=True, post_normalize=True, savefile=outfile)

        return svd

    # 
    def load_recsys_svd(self, k=100, min_values=2, recreate=False, verbose=True):
        import recsys.algorithm
        if verbose:
            recsys.algorithm.VERBOSE = True

        from recsys.algorithm.factorize import SVD

        # if there's already an svd file, load it
        # otherwise create the data from scratch
        tastings_svd_file = self.file_location(self.tastings_recsys_svd_filename)
        if recreate == False and os.path.isfile(tastings_svd_file):
            svd = SVD(self.tastings_recsys_svd_filename)
        else:
            svd = self.create_tastings_recsys_svd_data(k=k, min_values=min_values, verbose=verbose)

        # return the recsys SVD object, ready to make some recommendations...
        return svd

