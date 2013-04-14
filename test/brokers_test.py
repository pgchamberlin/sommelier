#!python
import unittest
from mock import Mock, MagicMock
from brokers import WineBroker, AuthorBroker, SommelierBroker

# Simple tests to make sure that the brokers call the db how we want them to, i.e.
# using and templating their queries as we expect
class BrokersTest(unittest.TestCase):

    def setUp(self):
        dbmock = {}
        self.sommelier_broker = WineBroker()
        self.sommelier_broker.db.execute = MagicMock()
        self.sommelier_broker.db.fetch_all = MagicMock()
        self.sommelier_broker.db.fetch_one = MagicMock()
        self.wine_broker = WineBroker()
        self.wine_broker.db.execute = MagicMock()
        self.wine_broker.db.fetch_all = MagicMock()
        self.wine_broker.db.fetch_one = MagicMock()
        self.author_broker = AuthorBroker()
        self.author_broker.db.execute = MagicMock()
        self.author_broker.db.fetch_all = MagicMock()
        self.author_broker.db.fetch_one = MagicMock()
 
    def test_get_authors(self):
        authors = self.sommelier_broker.get_authors()
        expected_query = self.sommelier_broker.authors_query
        self.sommelier_broker.db.execute.asset_called_once_with(expected_query)
        self.sommelier_broker.db.fetch_all.assert_called_once()
    
    def test_get_wines(self):
        authors = self.sommelier_broker.get_wines()
        expected_query = self.sommelier_broker.wines_query
        self.sommelier_broker.db.execute.asset_called_once_with(expected_query)
        self.sommelier_broker.db.fetch_all.assert_called_once()
    
    def test_get_wine_page(self):
        page = self.wine_broker.get_page(1)
        expected_query = self.wine_broker.wines_page_query.format(50, 0)
        self.wine_broker.db.execute.assert_called_once_with(expected_query)
        self.wine_broker.db.fetch_all.assert_called_once_with()
    
    def test_get_wine_num_pages(self):
        numpages = self.wine_broker.get_num_pages()
        expected_query = self.wine_broker.wines_count_query
        self.wine_broker.db.execute.assert_called_once_with(expected_query)
        self.wine_broker.db.fetch_one.assert_called_once_with()
    
    def test_get_wine(self):
        wine = self.wine_broker.get_wine(123)
        expected_query = self.wine_broker.wine_query.format(123)
        self.wine_broker.db.execute.assert_called_once_with(expected_query)
        self.wine_broker.db.fetch_one.assert_called_once_with()
     
    def test_get_author_page(self):
        page = self.author_broker.get_page(1)
        expected_query = self.author_broker.authors_page_query.format(50, 0)
        self.author_broker.db.execute.assert_called_once_with(expected_query)
        self.author_broker.db.fetch_all.assert_called_once_with()
    
    def test_get_author_num_pages(self):
        numpages = self.author_broker.get_num_pages()
        expected_query = self.author_broker.authors_count_query
        self.author_broker.db.execute.assert_called_once_with(expected_query)
        self.author_broker.db.fetch_one.assert_called_once_with()
    
    def test_get_author(self):
        author = self.author_broker.get_author(123)
        expected_query = self.author_broker.author_query.format(123)
        self.author_broker.db.execute.assert_called_once_with(expected_query)
        self.author_broker.db.fetch_one.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

