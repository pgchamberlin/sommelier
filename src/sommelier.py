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
            'type': 'list', 
            'self': {
                'title': 'Sommelier',
                'link': '/'
            },
            'list': [
                {
                'title': 'All Wines',
                'link': '/wines/1'
                },
                {
                'title': 'All Authors',
                'link': '/authors/1'
                }
            ]
        })

    def wine_page(self, page_num):
        records = self.broker.get_wine_page(page_num)
        if not records:
            return self.http_not_found_json()
        num_pages = self.broker.get_num_wine_pages()
        wines_list = []
        for wine in records:
            wines_list.append({
                'title': '{} {}'.format(wine['name'], wine['vintage']),
                'link': '/wine/{}'.format(wine['id'])
            })
        return self.http_success_json({
            'type': 'list', 
            'self': {
                'title': 'Wines, Page {}'.format(page_num),
                'link': '/wines/{}'.format(page_num)
            },
            'list': wines_list
        })

    def wine(self, wine_id):
        record = self.broker.get_wine(wine_id)
        if not record:
            return self.http_not_found_json()
        tastings_list = []
        for tasting in record['tastings']:
            tastings_list.append({
                'rating': tasting['rating'],
                'notes': tasting['notes'],
                'tasting_date': tasting['tasting_date'],
                'author': {
                    'title': tasting['author'],
                    'link': '/author/{}'.format(tasting['author_id'])
                }
            })
        wines = self.recommender.wines_for_wine(wine_id)
        wines_list = []
        for wine in wines:
            wines_list.append({
                'title': '{} {}'.format(wine['name'], wine['vintage']),
                'link': '/wine/{}'.format(wine['id'])
            })                
        return self.http_success_json({
            'type': 'wine',
            'self': {
                'title': '{} {}'.format(record['name'], record['vintage']),
                'name': record['name'],
                'vintage': record['vintage'],
                'grape_variety': record['grape_variety'],
                'appellation': record['appellation'],
                'sub_region': record['sub_region'],
                'region': record['region'],
                'country': record['country'],
                'producer': record['producer'],
                'tastings': tastings_list,
                'link': '/wine/{}'.format(record['id'])
            },
            'related_content': {
                'similar_wines': wines_list
            }
        })
    
    def author_page(self, page_num):
        records = self.broker.get_author_page(page_num)
        if not records:
            return self.http_not_found_json()
        num_pages = self.broker.get_num_author_pages()
        authors_list = []
        for author in records:
            authors_list.append({
                'title': author['name'],
                'link': '/author/{}'.format(author['id'])
            })
        return self.http_success_json({
            'type': 'list', 
            'self': {
                'title': 'Authors, Page {}'.format(page_num),
                'link': '/authors/{}'.format(page_num)
            },
            'list': authors_list
        })

    def author(self, author_id):
        author_id = int(author_id)
        record = self.broker.get_author(author_id)
        if not record:
            return self.http_not_found_json()
        tastings_list = []
        for tasting in record['tastings']:
            tastings_list.append({
                'rating': tasting['rating'],
                'notes': tasting['notes'],
                'tasting_date': tasting['tasting_date'],
                'wine': {
                    'title': '{} {}'.format(tasting['wine'], tasting['vintage']),
                    'link': '/wine/{}'.format(tasting['wine_id'])
                }
            })
        wines = self.recommender.wines_for_author(author_id)
        wines_list = []
        for wine in wines:
            wines_list.append({
                'title': '{} {}'.format(wine['name'], wine['vintage']),
                'link': '/wine/{}'.format(wine['id'])
            })                
        authors = self.recommender.authors_for_author(author_id)
        authors_list = []
        for author in authors:
            authors_list.append({
                'title': author['name'],
                'link': '/author/{}'.format(author['id'])
            })                
        return self.http_success_json({
            'type': 'author',
            'self': {
                'title': record['name'],
                'name': record['name'],
                'tastings': tastings_list,
                'link': '/author/{}'.format(record['id'])
            },
            'related_content': {
                'recommended_wines': wines_list,
                'similar_authors': authors_list
            }
        })

