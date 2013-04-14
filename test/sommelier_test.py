#!python
import unittest
from mock import Mock, MagicMock
from brokers import SommelierBroker
from recommender import Recommender
from sommelier import Sommelier

# Tests for the sommelier class, making sure it returns the right content in the 
# right format for each request, and that its auxiliary methods, like
# http_success_json() work properly

class SommelierTest(unittest.TestCase):

    def setUp(self):
        mock_broker = MagicMock()
        mock_broker.get_wine_page = MagicMock(return_value={'items':['item','item']})
        mock_broker.get_num_wine_pages = MagicMock(return_value=23)
        mock_broker.get_author_page = MagicMock(return_value={'items':['item','item']})
        mock_broker.get_num_author_pages = MagicMock(return_value=23)
        mock_broker.get_wine = MagicMock(return_value={'wine':'a wine'})
        mock_broker.get_author = MagicMock(return_value={'author':'an author'})
        mock_recommender = MagicMock()
        mock_recommender.wines_for_wine = MagicMock(return_value=['wine','wine','wine'])
        mock_recommender.wines_for_author = MagicMock(return_value=['wine for author','wine','wine'])
        self.sommelier = Sommelier(b=mock_broker, r=mock_recommender)
 
    def test_http_success_json(self):
        # method takes any dict as input
        test_content = { 'test': 'test content' }
        # should convert that dict into a UTF-8 JSON string, returned as first item of tuple
        expected_content = u'{"test": "test content"}'
        # also expected to return a dict with HTTP status and MIME Type parameters
        # - these will be converted to keyed arguments to Response() later using **
        expected_keyed_args_dict = { 'status': 200, 'mimetype': 'application/json; charset=utf-8' }
        response_body, keyed_args_dict = self.sommelier.http_success_json(test_content)
        self.assertEqual(expected_content, response_body)
        self.assertEqual(expected_keyed_args_dict, keyed_args_dict)

    def test_wines_page(self):
        expected_response_body = u'{"num_pages": 23, "wines": {"items": ["item", "item"]}}'
        response_body, keyed_args_dict = self.sommelier.wine_page(1)
        self.assertEqual(expected_response_body, response_body)

    def test_wine(self):
        expected_response_body = u'{"recommendations": ["wine", "wine", "wine"], "wine": {"wine": "a wine"}}'
        response_body, keyed_args_dict = self.sommelier.wine(123)
        self.assertEqual(expected_response_body, response_body)

    def test_authors_page(self):
        expected_response_body = u'{"num_pages": 23, "authors": {"items": ["item", "item"]}}'
        response_body, keyed_args_dict = self.sommelier.author_page(1)
        self.assertEqual(expected_response_body, response_body)

    def test_author(self):
        expected_response_body = u'{"recommendations": ["wine for author", "wine", "wine"], "author": {"author": "an author"}}'
        response_body, keyed_args_dict = self.sommelier.author(123)
        self.assertEqual(expected_response_body, response_body)

