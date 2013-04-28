#!python
import unittest
from mock import Mock, MagicMock

# import all our recommenders...
from recommender import SommelierRecommender, SommelierPearsonCFRecommender, SommelierYeungMFRecommender, SommelierTextMFRecommender, SommelierRecsysSVDRecommender

# Tests for the sommelier recommender class

class YeungMFRecommenderTest(unittest.TestCase):

    dummy_rating_data = [
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
        mock_broker.get_tastings = MagicMock(return_value=self.dummy_rating_data)
        mock_broker.get_wine_ids = MagicMock(return_value=self.dummy_wine_ids)
        self.recommender = SommelierYeungMFRecommender(b=mock_broker)
 
    def test_generate_lists_ui_matrix(self):
        generated_matrix = self.recommender.generate_lists_ui_matrix()
        self.assertEqual(self.expected_lists_matrix, generated_matrix)

    def test_create_lists_ui_matrix(self):
        self.recommender.generate_lists_ui_matrix = MagicMock()
        self.recommender.save_json_file = MagicMock()
        self.recommender.create_lists_ui_matrix()
        self.recommender.generate_lists_ui_matrix.assert_called_once()
        self.recommender.save_json_file.assert_called_once()

