#!python
import unittest
from mock import Mock, MagicMock
from brokers import WineBroker, AuthorBroker, SommelierBroker
from recommender import Recommender
from sommelier import Sommelier

# Simple tests to make sure that the brokers call the db how we want them to, i.e.
# using and templating their queries as we expect
class SommelierTest(unittest.TestCase):

    def setUp(self):
        dbmock = {}
        mock_broker = MagicMock()
        mock_broker.get_page = MagicMock(return_value={'items':['item','item']})
        mock_broker.get_num_pages = MagicMock(return_value=23)
        mock_broker.get_wine = MagicMock(return_value={'wine':'a wine'})
        mock_broker.get_author = MagicMock(return_value={'author':'an author'})
        mock_recommender = MagicMock()
        mock_recommender.wines_for_wine = MagicMock(return_value=['wine','wine','wine'])
        mock_recommender.wines_for_author = MagicMock(return_value=['wine for author','wine','wine'])
        self.sommelier = Sommelier(wb=mock_broker, ab=mock_broker, r=mock_recommender)
 
    def test_http_success_json(self):
        test_content = { 'test': 'test content' }
        expected_content = u'{"test": "test content"}'
        expected_keyed_args_dict = { 'status': 200, 'mimetype': 'application/json; charset=utf-8' }
        response_body, keyed_args_dict = self.sommelier.http_success_json(test_content)
        self.assertEqual(expected_content, response_body)
        self.assertEqual(expected_keyed_args_dict, keyed_args_dict)

    def test_wines_page(self):
        expected_response_body = u'{"num_pages": 23, "wines": {"items": ["item", "item"]}}'
        response_body, keyed_args_dict = self.sommelier.wines_page(1)
        self.assertEqual(expected_response_body, response_body)

    def test_wine(self):
        expected_response_body = u'{"recommendations": ["wine", "wine", "wine"], "wine": {"wine": "a wine"}}'
        response_body, keyed_args_dict = self.sommelier.wine(123)
        self.assertEqual(expected_response_body, response_body)

    def test_authors_page(self):
        expected_response_body = u'{"num_pages": 23, "authors": {"items": ["item", "item"]}}'
        response_body, keyed_args_dict = self.sommelier.authors_page(1)
        self.assertEqual(expected_response_body, response_body)

    def test_author(self):
        expected_response_body = u'{"recommendations": ["wine for author", "wine", "wine"], "author": {"author": "an author"}}'
        response_body, keyed_args_dict = self.sommelier.author(123)
        self.assertEqual(expected_response_body, response_body)

