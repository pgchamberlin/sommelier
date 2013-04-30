#!python

# I load a whole load of dependencies at the top here. 
# Obviously there is overhead involved in calling in all this stuff
# but for the sake manageability I'm putting it all up here ;-)

# general
from __future__ import division
import os
import collections
import json
import time

# text/language processing
import re
import nltk
from nltk.corpus import stopwords

# maths!
import numpy
from numpy import random
import scipy

# recsys-svd
import recsys.algorithm
from recsys.algorithm.factorize import SVD
from recsys.evaluation.prediction import MAE, RMSE

# Sommelier libs
from broker import SommelierBroker

# Abstract / interface class to define methods
# for recommendation provider classes
class SommelierRecommender:

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    def wines_for_author(self, author_id):
        return []

    def authors_for_author(self, author_id):
        return []

    def wines_for_wine(self, item_id):
        return []

    def impute_to_file(self, tastings):
        return []

    def data_file_directory(self):
        return "".join([os.getcwd(), '/data/'])

    def file_location(self, filename):
        return "".join([self.data_file_directory(), filename])

    def save_json_file(self, filename, data):
        thefile = "".join([self.data_file_directory(), filename, '.json'])
        with open(thefile, 'w') as outfile:
            json.dump(data, outfile)

    def load_json_file(self, filename):
        print "".join(["Loading ", self.data_file_directory(), filename, '.json'])
        return json.loads(open("".join([self.data_file_directory(), filename])).read())

    # Preferences are returned as a dictionary of indexed lists of ratings, accompanied
    # by a list of column ids which correspond to the ratings lists
    #
    # preferences = {
    #   row_id: [ rating_1, rating_2, .. rating_N ]
    # }
    #
    # column_ids = [ itemid_1, itemid_2, .. itemid_N ]
    #
    # @returns ( {} preferences, [] item_ids )
    def preferences(self, tastings, row_key, column_key, rating_key='rating'):
        if len(tastings) == 0:
            # if there aren't any tastings then bail out...
            return {}, []
        preferences = {}
        column_data = {}
        column_ids = []
        for tasting in tastings:
            # tastings should be ordered by author and wine
            preferences.setdefault(tasting[row_key], [])
            column_data.setdefault(tasting[column_key], {})
            column_data[tasting[column_key]].setdefault(tasting[row_key], tasting[rating_key])
        for column in column_data:
            for item in preferences.keys():
                if item in column_data[column].keys():
                    preferences[item].append(column_data[column][item])
                else:
                    preferences[item].append(0)
                if column not in column_ids:
                    column_ids.append(column)
        return preferences, column_ids

    def pearson_r(self, preferences, key_a, key_b):
        # get mutually rated items into two lists of ratings
        items_a = []
        items_b = []
        # iterate over all items
        for i in range(0, len(preferences[key_a])):
            # if both a and b have rated the item then add it to their item lists
            if preferences[key_a][i] != 0 and preferences[key_b][i] != 0:
                items_a.append(preferences[key_a][i])
                items_b.append(preferences[key_b][i])
        if len(set(items_a)) <= 1 or len(set(items_b)) <= 1:
            # one of the sets has standard deviation of 0 so pearson_r
            # will be NaN - in this case return 0.0
            return 0.0
        if len(items_a) < 3:
            # no items in common = no correlation
            # less than 3 items in common = problematic for comparison
            return 0.0
        # we now how two lists of ratings for the same items
        # these can be fed into the scipy.stats pearson r method
        # we only want the first value [0] from the method as we
        # don't need the 2-tail p value.
        return scipy.stats.pearsonr(items_a, items_b)[0]

    # Calculates mean absolute error for each row in the matrix
    # using the MAE() class from python-recsys
    # python-recsys evaluation documentation:
    # http://ocelma.net/software/python-recsys/build/html/evaluation.html
    def evaluate_matrices_mae(self, original_matrix, imputed_matrix):
        return self.evaluate_matrices(original_matrix, imputed_matrix, evaluator=MAE())
    
    def evaluate_matrices_rmse(self, original_matrix, imputed_matrix):
        return self.evaluate_matrices(original_matrix, imputed_matrix, evaluator=RMSE())

    def recsys_evaluate_matrices(self, original_matrix, imputed_matrix, evaluator=MAE()):
        total_error = 0
        total_rows = 0
        errors = ()
        for row_i, row in enumerate(original_matrix):
            # For each row build its list of non-zero values
            # Build a corresponding list of values for the imputed matrix
            row_values = []
            imputed_values = []
            for col_i, col in enumerate(row):
                if row[col_i] > 0:
                    row_values.append(col)
                    imputed_values.append(imputed_matrix[row_i][col_i])
            if len(row_values) == 0 or len(imputed_values) == 0:
                continue
            evaluator.load_ground_truth(row_values)
            evaluator.load_test(imputed_values)
            row_error = evaluator.compute()
            errors = errors + (row_error, )
            total_error += row_error
            total_rows += 1
        mean_total_error = total_error / total_rows
        return errors, mean_total_error

# This class implements recommendations largely based on the 
# basic user-user, user-item and item-item methods
# detailed by Segaran (2007, Ch.2)
class SommelierPearsonCFRecommender(SommelierRecommender):

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    # using a weighted average
    def wines_for_author(self, author_id, max_items=5):
        preferences, wine_ids = self.author_preferences(author_id)
        rankings = self.sorted_rankings(author_id, preferences, max_items)
        recommended_wine_ids = [ wine_ids[i] for r, i in rankings ]
        return self.broker.get_wines_by_id(recommended_wine_ids)

    def authors_for_author(self, author_id, max_items=5):
        preferences, wine_ids = self.author_preferences(author_id)
        return self.sorted_similarities(author_id, preferences)

    def wines_for_wine(self, wine_id, max_items=5):
        preferences, wine_ids = self.wine_preferences(wine_id)
        rankings = self.sorted_rankings(wine_id, preferences, max_items=5)
        recommended_wine_ids = [ wine_ids[i] for r, i in rankings ]
        return self.broker.get_wines_by_id(recommended_wine_ids)

    def author_preferences(self, author_id):
        tastings = self.broker.get_comparable_author_tastings(author_id)
        return self.preferences(tastings, 'author_id', 'wine_id')

    def wine_preferences(self, wine_id):
        tastings = self.broker.get_comparable_wine_tastings(wine_id)
        return self.preferences(tastings, 'wine_id', 'author_id')

    def sorted_similarities(self, subject_id, preferences, max_items=5):
        similarities = []
        for item_id in preferences.keys():
            if item_id == subject_id:
                # we don't need to compare our subject with itself
                continue
            similarity = self.pearson_r(preferences, subject_id, item_id)
            # only return positive correlations
            if similarity > 0:
                similarities.append((item_id, similarity))
        sorted_similarities = sorted(similarities, key=lambda sim: sim[1], reverse=True)
        return sorted_similarities[0:max_items]

    def sorted_rankings(self, subject_id, preferences, max_items=5):
        totals = {}
        similarity_sums = {}
        subject_preferences = preferences[subject_id]
        for other in preferences.keys():
            if other == subject_id:
                # don't compare subject to themself
                continue
            similarity = self.pearson_r(preferences, subject_id, other)
            if similarity <= 0:
                # no similarity is a waste of time
                continue
            for i in range(0, len(preferences[other])):
                if preferences[subject_id][i] == 0 and preferences[other][i] > 0:
                    totals.setdefault(i, 0)
                    totals[i] += preferences[other][i] * similarity
                    similarity_sums.setdefault(i, 0)
                    similarity_sums[i] += similarity
        if not totals:
            # there are no recommendations to be made :-(
            return ()
        rankings = [(total/similarity_sums[item], item) for item, total in totals.items()]
        return sorted(rankings, key=lambda sim: sim[0], reverse=True )[0:max_items]

# Implements SommelierRecommender using 
# python-recsys SVD library to make recommendations
class SommelierRecsysSVDRecommender(SommelierRecommender):

    # filename for raw tasting data in format used by MovieLens
    # format (rows): UserId::ItemId::Rating::UnixTime
    tastings_movielens_format = 'tastings_movielens_format'

    # filename for python-recsys zip outfile
    tastings_recsys_svd = 'recsys_svd_data'

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    def wines_for_author(self, author_id):
        svd = self.load_recsys_svd(k=100, min_values=3, verbose=False)
        # there may not be recommendations for this author, which would
        # raise a KeyError. We don't want a KeyError, an empty list is fine!
        try:
            recommendations = svd.recommend(int(author_id), is_row=False)
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

    def authors_for_author(self, author_id):
        return []

    def wines_for_wine(self, wine_id):
        svd = self.load_recsys_svd()
        # there may not be recommendations for this author, which would
        # raise a KeyError. We don't want a KeyError, an empty list is fine!
        try:
            # get similar wines, but pop() the first item off as it is the current wine
            recommendations = svd.similar(int(wine_id))
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

    # Decomposes the matrix of tastings data using recsys-svd's SVD()
    # and saves the output matices etc. to a zip file using SVD()'s built-in method
    def impute_to_file(self, tastings, k=100, min_values=2, verbose=True):
        # create a data file in Movielens format with the tastings data
        self.save_tastings_to_movielens_format_file(tastings)
        # for logging/testing purposes we may like this verbose
        if verbose:
            recsys.algorithm.VERBOSE = True
        svd = SVD()
        # load source data, perform SVD, save to zip file
        source_file = self.file_location(self.tastings_movielens_format)
        svd.load_data(filename=source_file, sep='::', format={'col':0, 'row':1, 'value':2, 'ids': int})
        outfile = self.file_location(self.tastings_recsys_svd)
        svd.compute(k=k, min_values=min_values, pre_normalize=None, mean_center=True, post_normalize=True, savefile=outfile)
        return svd
    
    def save_tastings_to_movielens_format_file(self, tastings):
        # make a list of strings which will be the lines in our 
        # Movielens format data file. The format is:
        # AuthorId::WineId::Rating::Timestamp
        import time
        outfile = self.file_location(self.tastings_movielens_format)
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

    # loads a recsys-svd data file stored to disk by the impute_to_file() method
    def load_recsys_svd(self):
        from recsys.algorithm.factorize import SVD
        svd = []
        # if there's an svd file, load it - otherwise we're out of luck as
        # we don't want to build these matrices at runtime!
        tastings_svd_file = self.file_location(self.tastings_recsys_svd)
        if recreate == False and os.path.isfile(tastings_svd_file):
            svd = SVD(tastings_svd_file)
        # return the recsys SVD object, ready to make some recommendations...
        return svd

# Implements SommelierRecommender using
# Albert Yeung's example Matrix Factorization code
# combined with basic CF techniques outlined in
# Segaran's "Collective Intelligence" (2007, Ch. 2)
class SommelierYeungMFRecommender(SommelierRecommender):

    # filename for user/item matrix in lists format
    # format: [[1,2,3][4,5,6]..]
    original_matrix = "tastings_yeung_matrix"

    # filename for factored and reconstructed matrix, using Yeung's simple MF algorithm
    # format: [[1,2,3][4,5,6]..]
    reconstructed_matrix = "reconstructed_yeung_matrix_k{}_steps{}"

    factors_matrix = "imputed_yeung_factors_k{}_steps{}"

    weights_matrix = "imputed_yeung_weights_k{}_steps{}"   

    multiple_factorization_metas = "multiple_factorization_metas_k{}_steps{}"   

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    def wines_for_author(self, author_id):
        return []

    def authors_for_author(self, author_id):
        return []

    def wines_for_wine(self, item_id):
        return []

    def impute_to_file(self, tastings):
        matrix = self.generate_lists_ui_matrix(tastings)
        factored_matrix = self.yeung_factor_matrix(matrix, steps=100, factors=10, evaluator='MAE')[0]
        return []

    # load the sparse ui matrix from disk
    def load_lists_ui_matrix(self):
        return self.load_json_file(self.original_matrix)

    def generate_lists_ui_matrix(self, tastings={}):
        if not tastings:
            # get all the tastings from the database
            tastings = self.broker.get_tastings()
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
        self.save_json_file(self.original_matrix, lists_matrix)
        return lists_matrix

    # Copied from Albert Yeung: http://www.quuxlabs.com/wp-content/uploads/2010/09/mf.py_.txt
    # This method factors the given matrix into
    def yeung_factor_matrix(self, matrix=[], steps=5000, factors=10, evaluator=MAE()):
        if not matrix:
            print "Loading sparse matrix..."
            matrix = self.load_lists_ui_matrix()
            print "Done."
        print "Converting to numpy.array()..."
        R = numpy.array(matrix)
        print "Done."
        N = len(R)
        M = len(R[0])
        K = factors
        print "Creating random matrices..."
        P = numpy.random.rand(N, K)
        Q = numpy.random.rand(M, K)
        print "Done."
        print "Beginning matrix factorization..."
        nP, nQ, e = self.yeung_matrix_factorization(R, P, Q, K, steps)
        print "Done."
        print "Final error: {}".format(e)
        self.save_json_file(self.factors_matrix.format(K, steps), nP.tolist())
        self.save_json_file(self.weights_matrix.format(K, steps), nQ.tolist())
        print "Dotting generated matrices..."
        nR = numpy.dot(nP, nQ.T)
        print "Done."
        print "Evaluation using {}...".format(evaluator.__class__.__name__)
        errors, mean_total_error = self.recsys_evaluate_matrices(R, nR, evaluator)
        print "Mean total error: {}".format(mean_total_error)
        print "Saving to JSON file..."
        self.save_json_file(self.reconstructed_matrix.format(K, steps), nR.tolist())
        print "Done."
        return nR, nP, nQ, errors, mean_total_error

    # Copied from Albert Yeung: http://www.quuxlabs.com/wp-content/uploads/2010/09/mf.py_.txt
    def yeung_matrix_factorization(self, R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
        print "Matrix Factorization"
        print "Steps: {}".format(steps)
        print "Factors: {}".format(K)
        Q = Q.T
        s = 0
        for step in xrange(steps):
            s+=1
            print "Step {} / {}".format(s,steps)
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
            print "Error: {}".format(e)
            if e < 0.001:
                break
        return P, Q.T, e

    # Will run any number of Yeung factorizations of a matrix, iterating over 
    # a list of configuration argument dicts to be passed to the factorization method
    def multiple_factorizations(self, matrix, config_args):
        metas = []
        for args in config_args:
            start = int(time.time())
            fm = self.yeung_factor_matrix(matrix, **args)
            end = int(time.time())
            # get metas from result
            ue = fm[3]
            te = fm[4]
            t = end - start
            metas.append({"args": args, "user_errors": ue, "total_errors": te, "execution_time_seconds": t})
            self.save_json_file(self.multiple_factorization_metas.format(args["factors"], args["steps"]), metas)
        return metas

# Implements SommelierRecommender performing
# matrix decomposition based around word frequency to
# generate topics which can be used to predict similarities
# between wines based on the language used about them, and
# between authors based on the language they use. Similar to
# the techniques outlined by Segaran in "Collective 
# Intelligence" (2007, Ch. 10), but applied in a different
# context.
class SommelierTextMFRecommender(SommelierYeungMFRecommender):

    # filename for user/item matrix in lists format
    # format: [[1,2,3][4,5,6]..]
    original_matrix = "tastings_text_mf_matrix"

    # filename for factored and reconstructed matrix, using Yeung's simple MF algorithm
    # format: [[1,2,3][4,5,6]..]
    reconstructed_matrix = "reconstructed_text_mf_matrix"

    factors_matrix = "imputed_text_mf_factors"

    weights_matrix = "imputed_text_mf_weights"   

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    def wines_for_author(self, author_id):
        return []

    def authors_for_author(self, author_id):
        return []

    def wines_for_wine(self, item_id):
        return []

    def impute_to_file(self, tastings, steps=5000):
        matrix = self.get_tastings_word_matrix(tastings)
        self.save_json_file(self.original_matrix, matrix)
        self.yeung_factor_matrix(matrix=matrix, steps=steps)
        return matrix

    # one row for each tasting, one column for each word
    # with counts of occurrences of the word in the tasting note
    def get_tastings_word_matrix(self, tastings):
        words = self.get_words(tastings)
        rows = []
        for t in tastings:
            row = []
            t_words = re.split('\W+', t['notes'])
            for w in words:
                row.append(t_words.count(w))
            rows.append(row)
        return rows

    def get_words(self, tastings):
        words = []
        dist = self.tastings_frequency_distribution(tastings, min_values=4)
        for w in dist:
            words.append(w)
        return words

    # gets all words metioned >= min_values times, excluding stopwords
    def tastings_frequency_distribution(self, tastings, min_values=4):
        words = []
        for tasting in tastings:
            words += re.split('\W+', tasting['notes'])
        filtered_words = [w.lower() for w in words if not w in stopwords.words('english')]
        dist = nltk.FreqDist(filtered_words)
        words = dist.samples()
        for w in words:
            if dist[w] < min_values:
                dist.pop(w)
        return dist

