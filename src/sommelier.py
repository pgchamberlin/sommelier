#!python

# import useful Flask libs
from flask import request, Response, jsonify, json

# import broker libs that will interface with the DB
from broker import SommelierBroker

# import the Sommelier recommender
from recommender import SommelierPearsonCFRecommender, SommelierRecsysSVDRecommender

class Sommelier():

    def __init__(self, b=SommelierBroker(), r=SommelierRecsysSVDRecommender()):
        self.broker = b
        self.recommender = r

    # Takes dict of content and generates JSON response with
    # appropriate MIME type, HTTP status code etc.
    def http_success_json(self, content):
        response = json.dumps(content, encoding="utf-8")
        response = ''.join(response.decode('unicode-escape').splitlines())
        return response, { 'status': 200, 'mimetype': 'application/json; charset=utf-8' }

    def http_not_found_json(self):
        response = json.dumps("404: Not found", encoding="utf-8")
        return response, { 'status': 404, 'mimetype': 'application/json; charset=utf-8' }

    def index(self):
        return self.http_success_json({
            'self': {
                'title': 'Sommelier'
            },
            'links': {
                'wines': '/wines/1',
                'authors': '/authors/1',
            }
        })

    def wine_page(self, page_num):
        records = self.broker.get_wine_page(page_num)
        if not records:
            return self.http_not_found_json()
        num_pages = self.broker.get_num_wine_pages()
        return self.http_success_json({
            'self': {
                'title': 'Wines page {}'.format(page_num),
                'wines': records,
            },
            'next_page': '/wines/{}'.format(page_num + 1) if num_pages > page_num else 'none',
            'previous_page': '/wines/{}'.format(page_num - 1) if page_num != 1 else 'none',
        })

    def wine(self, wine_id):
        record = self.broker.get_wine(wine_id)
        if not record:
            return self.http_not_found_json()
        recommendations = self.recommender.wines_for_wine(wine_id)
        return self.http_success_json({
            'self': {
                'title': 'Wine page: {} {}'.format(record['name'], record['vintage']),
                'wine': record,
            },
            'recommendations': recommendations
        })
    
    def author_page(self, page_num):
        records = self.broker.get_author_page(page_num)
        if not records:
            return self.http_not_found_json()
        num_pages = self.broker.get_num_author_pages()
        return self.http_success_json({
            'authors': records, 
            'num_pages': num_pages 
        })

    def author(self, author_id):
        author_id = int(author_id)
        record = self.broker.get_author(author_id)
        if not record:
            return self.http_not_found_json()
        wines = self.recommender.wines_for_author(author_id)
        authors = self.recommender.authors_for_author(author_id)
        return self.http_success_json({
            'author': record,
            'recommendations': {
                'wines': wines,
                'authors': authors
            }
        })

