#!python

# import useful Flask libs
from flask import request, Response, jsonify, json

# import broker libs that will interface with the DB
from brokers import WineBroker, AuthorBroker

# import the Sommelier recommender
from recommender import Recommender

class Sommelier:

    def __init__(self, wb=WineBroker(), ab=AuthorBroker(), r=Recommender()):
        self.wine_broker = wb
        self.author_broker = ab
        self.recommender = r

    # Takes dict of content and generates JSON response with
    # appropriate MIME type, HTTP status code etc.
    def http_success_json(self, content):
        response = json.dumps(content, encoding="utf-8")
        response = ''.join(response.decode('unicode-escape').splitlines())
        return response, { 'status': 200, 'mimetype': 'application/json; charset=utf-8' }

    def wines_page(self, page_num):
        records = self.wine_broker.get_page(page_num)
        num_pages = self.wine_broker.get_num_pages()
        return self.http_success_json({
            'wines': records,
            'num_pages': num_pages
        })

    def wine(self, wine_id):
        record = self.wine_broker.get_wine(wine_id)
        recommendations = self.recommender.wines_for_wine(wine_id)
        return self.http_success_json({
            'wine': record,
            'recommendations': recommendations
        })
                
    def authors_page(self, page_num):
        records = self.author_broker.get_page(page_num)
        num_pages = self.author_broker.get_num_pages()
        return self.http_success_json({
            'authors': records, 
            'num_pages': num_pages 
        })

    def author(self, author_id):
        record = self.author_broker.get_author(author_id)
        recommendations = self.recommender.wines_for_author(author_id)
        return self.http_success_json({
            'author': record,
            'recommendations': recommendations
        })

