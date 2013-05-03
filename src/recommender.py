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
import random
import math

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

# Abstract / base class to hold methods shared between all recommenders
class SommelierRecommenderBase:

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

    # Open a given file which is in Movielens format
    # and convert to tastings as used by Sommelier
    def load_movielens_to_tastings(self, filename):
        tastings = []
        print "Loading Movielens data... (this may take a while)"
        for line in open("".join([self.data_file_directory(), filename]), 'r'):
            tastings.append(self.movielens_line_to_tasting(line))
        print "Done."
        return tastings
            
    # Converts a live from a Movielens file (as a string)
    # to a tasting dict. This is for use in benchmarking and
    # evaluation so that Movielens data can be used to 
    # test the system. Movielens file format:
    # UserId::ItemId::Rating::Timestamp
    def movielens_line_to_tasting(self, line):
        if line.find("::") != -1:
            # this is double-colon separated
            user_id, item_id, rating, timestamp = line.split("::")
        elif line.find("\t") != -1:
            # presumably this is tab-separated
            user_id, item_id, rating, timestamp = line.split('\t')
        else:
            raise Exception("Cannot decode input string: {}".format(line))
        tasting = {
            'author_id': int(user_id),
            'wine_id': int(item_id),
            'rating': int(rating),
            'tasting_date': str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp))))
        }
        return tasting   

    def tastings_to_movielens_format(self, tastings, separator="::"):
        # make a list of strings which will be the lines in our 
        # Movielens format data file. The format is:
        # AuthorId::WineId::Rating::Timestamp
        lines = []
        for tasting in tastings:
            # if the date is not valid set to 0, otherwise convert to Unix epoch
            date = '0'
            if 'tasting_date' in tasting and tasting['tasting_date'] != '0000-00-00 00:00:00':
                date = str(time.mktime(time.strptime(tasting['tasting_date'], "%Y-%m-%d %H:%M:%S"))).encode('utf-8')
            lines.append("".join([
                str(tasting['author_id']).encode('utf-8'), separator, 
                str(tasting['wine_id']).encode('utf-8'), separator, 
                str(tasting['rating']).encode('utf-8'), separator, 
                date, '']))
        return lines

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
        mean_total_error = 0.0
        if total_rows > 0.0:
            mean_total_error = total_error / total_rows
        return errors, mean_total_error

# This class implements recommendations largely based on the 
# basic user-user, user-item and item-item methods
# detailed by Segaran (2007, Ch.2)
class SommelierPearsonCFRecommender(SommelierRecommenderBase):

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    # using a weighted average
    def wines_for_author(self, author_id, max_items=5):
        author_id = int(author_id)
        preferences, wine_ids = self.author_preferences(author_id)
        rankings = self.sorted_rankings(author_id, preferences, max_items)
        recommended_wine_ids = [ wine_ids[i] for r, i in rankings ]
        if len(recommended_wine_ids) > 0:
            return self.broker.get_wines_by_id(recommended_wine_ids)
        # if we couldn't find any wines to recommend, return empty
        return []
        

    def authors_for_author(self, author_id, max_items=5):
        author_id = int(author_id)
        preferences, wine_ids = self.author_preferences(author_id)
        return self.sorted_similarities(author_id, preferences)

    def wines_for_wine(self, wine_id, max_items=5):
        wine_id = int(wine_id)
        preferences, wine_ids = self.wine_preferences(wine_id)
        rankings = self.sorted_rankings(wine_id, preferences, max_items=5)
        recommended_wine_ids = [ wine_ids[i] for r, i in rankings ]
        if len(recommended_wine_ids) > 0:
            return self.broker.get_wines_by_id(recommended_wine_ids)
        # if we couldn't find any wines to recommend, return empty
        return []

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
        if subject_id not in preferences:
            # we can't recommend for this subject
            return []
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
class SommelierRecsysSVDRecommender(SommelierRecommenderBase):

    # filename for raw tasting data in format used by MovieLens
    # format (rows): UserId::ItemId::Rating::UnixTime
    tastings_movielens_format = 'tastings_movielens_format'

    # filename for python-recsys zip outfile
    tastings_recsys_svd = 'recsys_svd_data'

    def __init__(self, b=SommelierBroker()):
        self.broker = b

    def wines_for_author(self, author_id):
        svd = self.load_recsys_svd()
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
        movielens_lines = self.tastings_to_movielens_format(tastings)
        outfile = self.file_location(self.tastings_movielens_format)
        with open(outfile, 'w') as datafile:
            for line in movielens_lines:
                datafile.write(line)

    # loads a recsys-svd data file stored to disk by the impute_to_file() method
    def load_recsys_svd(self):
        from recsys.algorithm.factorize import SVD
        svd = []
        # if there's an svd file, load it - otherwise we're out of luck as
        # we don't want to build these matrices at runtime!
        tastings_svd_file = self.file_location(self.tastings_recsys_svd)
        if os.path.isfile(tastings_svd_file):
            svd = SVD(tastings_svd_file)
        # return the recsys SVD object, ready to make some recommendations...
        return svd

# Implements SommelierRecommender using
# Albert Yeung's example Matrix Factorization code
# combined with basic CF techniques outlined in
# Segaran's "Collective Intelligence" (2007, Ch. 2)
class SommelierYeungMFRecommender(SommelierRecommenderBase):

    # filename for user/item matrix in lists format
    # format: [[1,2,3][4,5,6]..]
    original_matrix = "tastings_yeung_matrix"

    # filename for user/item matrix in lists format
    # format: [[1,2,3][4,5,6]..]
    test_data_matrix = "tastings_yeung_test_matrix_{}percent"

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
        matrix = self.generate_lists_ui_matrix(tastings, self.original_matrix)
        factored_matrix = self.yeung_factor_matrix(matrix, steps=1000, factors=10, evaluator='MAE')[0]
        return []

    # load the sparse ui matrix from disk
    def load_lists_ui_matrix(self):
        matrix_data = self.load_json_file(self.original_matrix)
        matrix = matrix_data["ratings"]
        author_ids = matrix_data["author_ids"]
        wine_ids = matrix_data["wine_ids"]
        return matrix, author_ids, wine_ids

    def generate_lists_ui_matrix(self, tastings={}, outfile=''):
        if not tastings:
            # get all the tastings from the database
            tastings = self.broker.get_tastings()
        # make a dict with an entry for each author, with wines and ratings:
        # { author: { wine_id: rating, wine_id: rating, ... } ... }
        author_ratings = {}
        wine_ids = []
        for tasting in tastings:
            author_ratings.setdefault(tasting['author_id'], {})
            author_ratings[tasting['author_id']][tasting['wine_id']] = tasting['rating']
            if tasting['wine_id'] not in wine_ids:
                wine_ids.append(tasting['wine_id'])
        # for each author iterate over wines and make a tuple with ratings for each wine, or 0.0
        lists_matrix = []
        author_ids = []
        for author_id in author_ratings:
            author = author_ratings[author_id]
            author_ids.append(author_id)
            author_wine_list = []
            for wine_id in wine_ids:
                # if there is a key in the author dict for this wine, take the rating from that
                if wine_id in author:
                    author_wine_list.append(float(author[wine_id]))
                # otherwise append a 0.0
                else:
                    author_wine_list.append(0.0)
            lists_matrix.append(author_wine_list)
        if outfile:
            self.save_json_file(outfile, { "ratings": lists_matrix, "author_ids": author_ids, "wine_ids": wine_ids })
        return lists_matrix, author_ids, wine_ids

    # Copied from Albert Yeung: http://www.quuxlabs.com/wp-content/uploads/2010/09/mf.py_.txt
    # This method factors the given matrix into
    def yeung_factor_matrix(self, matrix=[], steps=5000, factors=10, evaluator=MAE(), verbose=True):
        if not matrix:
            matrix = self.load_lists_ui_matrix()
        R = numpy.array(matrix)
        N = len(R)
        M = len(R[0])
        K = factors
        P = numpy.random.rand(N, K)
        Q = numpy.random.rand(M, K)
        nP, nQ, e = self.yeung_matrix_factorization(R, P, Q, K, steps, verbose=verbose)
        if verbose: print "Final error: {}".format(e)
        self.save_json_file(self.factors_matrix.format(K, steps), nP.tolist())
        self.save_json_file(self.weights_matrix.format(K, steps), nQ.tolist())
        nR = numpy.dot(nP, nQ.T)
        if verbose: print "Saving to JSON file..."
        self.save_json_file(self.reconstructed_matrix.format(K, steps), nR.tolist())
        if verbose: print "Evaluation using {}...".format(evaluator.__class__.__name__)
        errors, mean_total_error = self.recsys_evaluate_matrices(R, nR, evaluator)
        if verbose: print "Mean total error: {}".format(mean_total_error)
        return nR, nP, nQ, errors, mean_total_error

    # Copied from Albert Yeung: http://www.quuxlabs.com/wp-content/uploads/2010/09/mf.py_.txt
    def yeung_matrix_factorization(self, R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02, verbose=True):
        if verbose:
            print "Matrix Factorization"
            print "Steps: {}".format(steps)
            print "Factors: {}".format(K)
        Q = Q.T
        s = 0
        for step in xrange(steps):
            s+=1
            if verbose: print "Step {} / {}".format(s,steps)
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
            if verbose: print "Error: {}".format(e)
            if e < 0.001:
                break
        return P, Q.T, e

    # Will run any number of Yeung factorizations of a matrix, iterating over 
    # a list of configuration argument dicts to be passed to the factorization method
    def multiple_factorizations(self, matrix, config_args):
        sparsity = self.sparsity_percent(matrix)
        print "Sparsity of matrix for multiple factorizations: {}%".format(sparsity)
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

    def predict_rating(self, imputed_matrix, authors, wines, author_id, wine_id):
        if author_id in authors:
            author_idx = authors.index(author_id)
            if wine_id in wines:
                wine_idx = wines.index(wine_id)
                if author_idx < len(imputed_matrix):
                    if wine_idx < len(imputed_matrix[author_idx]):
                        return imputed_matrix[author_idx][wine_idx]
                    raise Exception("Wine index out of bounds for matrix")
                raise Exception("Author index out of bounds for matrix")
            raise Exception("Wine index not found for imputed matrix")
        raise Exception("Author index not found for imputed matrix")

    # Get all tastings, randomly split into train and test portions
    # Generate a matrix for the test portion of the data
    # Factor this matrix using the **config_args passed into the method
    # Iterate over the training portion of the data, checking the
    # real ratings against those imputed by the factorization
    # Record MAE for each author, standard deviation of error for 
    # each author, total MAE, total standard deviation of error, 
    # and finally a normalised MAE for good measure...
    def split_data_evaluation(self, config_args, matrix_file=[], tastings=[], percent_train=80):
        print "Test/train split: {}/{}".format(percent_train, 100-percent_train)
        print "Randomly splitting tastings for testing..."
        train_tastings, test_tastings = self.split_train_test_tastings(tastings, percent_train)
        print "Generating matrix for testing..."
        train_matrix, author_ids, wine_ids = self.generate_lists_ui_matrix(train_tastings, self.test_data_matrix)
        print "num authors {}".format(len(train_matrix))
        print "num items {}".format(len(train_matrix[0]))
        for args in config_args:
            print "Evaluation for args: {}".format(args)
            imputed_matrix = self.yeung_factor_matrix(train_matrix, **args)[0]
            total_error = 0.0
            num_tastings = 0
            errors = []
            author_errors = {}
            missing_authors = 0
            missing_wines = 0
            for tasting in test_tastings:
                if tasting["author_id"] not in author_ids:
                    # there were no items for this author in the test data
                    missing_authors +=1
                    continue
                if tasting["wine_id"] not in wine_ids:
                    # there were no items for this wine in the test data
                    missing_wines += 1
                    continue
                prediction = self.predict_rating(imputed_matrix, author_ids, wine_ids, tasting["author_id"], tasting["wine_id"])
                rating = float(tasting['rating'])
                error = abs(rating - prediction)
                author_errors.setdefault(tasting['author_id'], [])
                author_errors[tasting['author_id']].append(error)
                errors.append(error)
                total_error += error
                num_tastings += 1
            print "Missing authors: {}, missing wines: {}".format(missing_authors, missing_wines)
            author_stds = {}
            for author_id in author_errors:
                # author standard deviation
                author_stds.setdefault(author_id, 0.0)
                author_stds[author_id] = numpy.std(author_errors[author_id])
            mae = total_error / num_tastings
            # we can get the mae as a normalised value (between 0 and 1) by dividing by the difference between the
            # highest and lowest rating which we know is (5 - 0) = 5
            nmae = mae / 5
            # total standard deviation
            total_std = numpy.std(errors)
            print "NMAE {}".format(nmae)
            print "MAE {}".format(mae)
            print "Total SD {}".format(total_std)
            print "Author SDs {}".format(author_stds)

    def split_data_evaluate_movielens_file(self, filepath, config_args, percent_train=80):
        tastings = self.load_movielens_to_tastings(filepath)
        print "Number of tastings: {}".format(len(tastings))
        self.split_data_evaluation(config_args, tastings=tastings, percent_train=percent_train)

    def split_train_test_tastings(self, tastings, percent_train=80):
        if percent_train > 100:
            raise Exception("percent_test must be 100 or less")
        num_tastings = len(tastings)
        num_train = math.ceil(num_tastings * ( percent_train / 100 ))
        # now create an array of length num_tastings, with num_test amount of 1s
        # randomly distributed within it
        ones = numpy.ones((num_train)).tolist()
        zeros = numpy.zeros((num_tastings - num_train)).tolist()
        ones_and_zeros = ones + zeros
        random.shuffle(ones_and_zeros)
        test_tastings = []
        train_tastings = []
        for tasting in tastings:
            if ones_and_zeros.pop() == 1:
                train_tastings.append(tasting)
            else:
                test_tastings.append(tasting)
        return train_tastings, test_tastings 

    def sparsity_percent(self, matrix):
        zero_count = 0.0
        total_count = 0.0
        for row in matrix:
            for col in row:
                total_count += 1.0
                if col == 0.0:
                    zero_count += 1.0
        return ( zero_count / total_count ) * 100.0


# Implements SommelierRecommender performing
# matrix decomposition based around word frequency to
# generate topics which can be used to predict similarities
# between wines based on the language used about them, and
# between authors based on the language they use. Similar to
# the techniques outlined by Segaran in "Collective 
# Intelligence" (2007, Ch. 10), but applied in a different
# context.
#
## UNIMPLEMENTED: THIS CLASS DOES NOT WORK ... YET
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

# Facade class for recommenders. May have specific recommender implementation
# injected into it or depend on default defined in its signature.
class SommelierRecommender:

    def __init__(self, b=SommelierBroker(), r=SommelierPearsonCFRecommender()):
        self.broker = b
        self.recommender = r

    def wines_for_author(self, author_id):
        return self.recommender.wines_for_author(author_id)

    def authors_for_author(self, author_id):
        return self.recommender.authors_for_author(author_id)

    def wines_for_wine(self, wine_id):
        return self.recommender.wines_for_wine(wine_id)

