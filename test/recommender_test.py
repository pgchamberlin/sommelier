#!python
import unittest
from mock import Mock, MagicMock

# import all our recommenders...
from recommender import SommelierRecommender, SommelierPearsonCFRecommender, SommelierYeungMFRecommender, SommelierTextMFRecommender, SommelierRecsysSVDRecommender

#
# Tests for the sommelier recommender class
# This does not test some very small methods, such as
# those for saving and retrieving JSON files
#
class RecommenderTest(unittest.TestCase):

    dummy_tastings = [
        { "author_id": 1, "wine_id": 5, "rating": 9 },
        { "author_id": 2, "wine_id": 6, "rating": 10 },
        { "author_id": 3, "wine_id": 7, "rating": 11 },
        { "author_id": 4, "wine_id": 8, "rating": 12 }]

    expected_preferences_1 = {
        1: [ 0, 9, 0, 0 ],
        2: [ 0, 0, 10, 0 ],
        3: [ 0, 0, 0, 11 ],
        4: [ 12, 0, 0, 0 ]
        }, [8, 5, 6, 7]

    expected_preferences_2 = {
        5: [ 9, 0, 0, 0 ],
        6: [ 0, 10, 0, 0 ],
        7: [ 0, 0, 11, 0 ],
        8: [ 0, 0, 0, 12 ]
        }, [1, 2, 3, 4]

    pearson_r_test_preferences = {
        "row_1": [ 1, 2, 3, 4, 5 ],
        "row_2": [ 2, 3, 4, 5, 6 ],
        "row_3": [ 5, 4, 3, 2, 1 ],
        "row_4": [ 3, 3, 3, 3, 3 ],
        "row_5": [ 1, 2 ],
        "row_6": [ 3, 1 ]}

    def setUp(self):
        mock_broker = MagicMock()
        self.recommender = SommelierRecommender(b=mock_broker)

    def test_pearson_r(self):
        # rows 1 and 2 have 100% positive correlation
        self.assertEqual(1.0, self.recommender.pearson_r(self.pearson_r_test_preferences, 'row_1', 'row_2'))

        # rows 1 and 3 have 100% negative correlation
        self.assertEqual(-1.0, self.recommender.pearson_r(self.pearson_r_test_preferences, 'row_1', 'row_3'))

        # row 4 has a standard deviation of 0, which we need to deal with to avoid a division by zero error
        # when the covariance is divided by the product of the standard deviations
        # in this case the method returns 0.0, on the basis that a user submitting the same rating for every 
        # item is not expressing any preference at all, so a neutral similarity score is appropriate
        self.assertEqual(0.0, self.recommender.pearson_r(self.pearson_r_test_preferences, 'row_1', 'row_4'))

        # cases where there are two or less items for comparison are problematic for pearson_r; any two
        # lists with 2 items will always result in either 1.0 or -1.0. That is not a useful score, as
        # there may be no similarity in the ratings at all, so we return 0.0 if there are < 3 items
        self.assertEqual(0.0, self.recommender.pearson_r(self.pearson_r_test_preferences, 'row_5', 'row_6'))

    def test_preferences(self):
        # preferences formatting for author rows / wine columns
        self.assertEqual(self.expected_preferences_1, self.recommender.preferences(self.dummy_tastings, 'author_id', 'wine_id')) 

        # preferences formatting for wine rows / author columns
        self.assertEqual(self.expected_preferences_2, self.recommender.preferences(self.dummy_tastings, 'wine_id', 'author_id')) 

#
#
#
class PearsonCFRecommenderTest(unittest.TestCase):

    def setUp(self):
        mock_broker = MagicMock()
        self.recommender = SommelierPearsonCFRecommender(b=mock_broker)

    # test args for both sorted_rankings and sorted_similarities
    # these consist of an id and a dict of user preferences of the format: { id: [ list, of, ratings ] }
    # In this test data user 1 has 3 ratings in common with the others, the first three (0, 1 and 2). 
    # Users 2, 3 and 4 have each rated the last two items (3 and 4), whereas user 1 has not.
    # Items 3 and 4 have been given identical rankings by users 2, 3 and 4 ...
    test_args = ( 1, { 1: [ 1, 2, 3, 0, 0 ], 2: [ 1, 2, 3, 3, 4 ], 3: [ 3, 2, 1, 3, 4 ], 4: [ 1, 2, 3, 3, 4 ] } )

    # ... so the rankings should be 4.0 for item 4 and 3.0 for item 3, with item 4 first in the list
    # as it has the higher rating
    sorted_rankings_expected = [(4.0, 4), (3.0, 3)]

    # covers recommender.sorted_rankings
    def test_sorted_rankings(self):
        self.assertEqual(self.sorted_rankings_expected, self.recommender.sorted_rankings(*self.test_args))

    # We can use the same arguments from above to test the sorted_similarities() method
    # this method will look at the pearson score for each of the users. The ratings in this
    # case are loaded so that users 2 and 4 have identical ratings as 1, so will be recommended
    # in that order. User 3 has inverse ratings to user 1, so they will score -1.0 and not
    # be returned by the method
    sorted_similarities_expected = [(2, 1.0), (4, 1.0)]

    # covers recommender.sorted_similarities
    def test_sorted_similarities(self):
        self.assertEqual(self.sorted_similarities_expected, self.recommender.sorted_similarities(*self.test_args))

class YeungMFRecommenderTest(unittest.TestCase):

    dummy_tastings = [
        { "author_id": 1, "wine_id": 1, "rating": 1 },
        { "author_id": 2, "wine_id": 2, "rating": 2 },
        { "author_id": 3, "wine_id": 3, "rating": 3 },
        { "author_id": 4, "wine_id": 4, "rating": 4 }]

    dummy_wine_ids = [
        { 'id': 1 },
        { 'id': 2 },
        { 'id': 3 },
        { 'id': 4 }]

    expected_lists_matrix = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 2.0, 0.0, 0.0],
        [0.0, 0.0, 3.0, 0.0],
        [0.0, 0.0, 0.0, 4.0]]

    def setUp(self):
        mock_broker = MagicMock()
        mock_broker.get_tastings = MagicMock(return_value=self.dummy_tastings)
        mock_broker.get_wine_ids = MagicMock(return_value=self.dummy_wine_ids)
        self.recommender = SommelierYeungMFRecommender(b=mock_broker)
 
    def test_generate_lists_ui_matrix(self):
        generated_matrix = self.recommender.generate_lists_ui_matrix()
        self.assertEqual(self.expected_lists_matrix, generated_matrix)

