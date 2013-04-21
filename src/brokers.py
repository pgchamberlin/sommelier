#!python
import math
from dbconnector import SommelierDbConnector

class SommelierBroker:

    rating_data_query = """
        SELECT *
        FROM tasting t
        WHERE author_id <> 0
    """
    wine_ids_query = """
        SELECT id 
        FROM wine w
        ORDER BY id ASC
        """
    wines_by_id_query = """
        SELECT *
        FROM wine w
        WHERE w.id
        IN ({})
    """
    wines_query = """
        SELECT * 
        FROM wine w
        ORDER BY id ASC
        """
    wine_page_query = """
        SELECT * 
        FROM wine w
        LIMIT {} OFFSET {}
        """
    wine_query  = """
        SELECT w.*, t.*, a.name AS author FROM wine w
        LEFT JOIN tasting t ON w.id = t.wine_id 
        LEFT JOIN author a ON t.author_id = a.id
        WHERE w.id = {}
        """
    wine_count_query = """
        SELECT COUNT(*) AS count FROM wine
        """
    authors_query = """
        SELECT * 
        FROM author a
        ORDER BY id ASC
        """
    author_ids_query = """
        SELECT id 
        FROM author a
        """
    author_page_query = """
        SELECT * 
        FROM author a
        LIMIT {} OFFSET {}
        """
    author_query  = """
        SELECT a.*, t.*, w.name as wine FROM author a
        JOIN tasting t ON t.author_id = a.id
        JOIN wine w ON t.wine_id = w.id
        WHERE a.id = {}
        """
    author_count_query = """
        SELECT COUNT(*) AS count FROM author a
        """
    page_size = 50

    def __init__(self, db=SommelierDbConnector()):
        self.db = db
    
    def get_rating_data(self):
        self.db.execute(self.rating_data_query)
        return self.db.fetch_all()

    def get_wines(self):
        self.db.execute(self.wines_query)
        return self.db.fetch_all()

    def get_wine_ids(self):
        self.db.execute(self.wine_ids_query)
        return self.db.fetch_all()

    def get_wines_by_id(self, wine_ids):
        self.db.execute(self.wines_by_id_query.format(",".join(map(str, wine_ids))))
        return self.db.fetch_all()

    def get_wine_page(self, pagenum=1):
        pageparams = self.page_size, self.page_size * (pagenum - 1)
        self.db.execute(self.wine_page_query.format(*pageparams))
        return self.db.fetch_all()

    def get_num_wine_pages(self):
        self.db.execute(self.wine_count_query)
        result = self.db.fetch_one()
        count = float( result['count'] );
        return int( math.ceil( count / self.page_size ) )

    def get_wine(self, wine_id):
        self.db.execute(self.wine_query.format(wine_id))
        result = self.db.fetch_one()
        if result is None: return {}
        wine = {
            'name': result['name'],
            'vintage': result['vintage'],
            'grape_variety': result['grape_variety'],
            'appellation': result['appellation'],
            'sub_region': result['sub_region'],
            'region': result['region'],
            'country': result['country'],
            'producer': result['producer'],
            'tastings': []
        }
        if result['author'] is not None:
            wine['tastings'].append({
                'author': result['author'],
                'notes': result['notes'],
                'rating': result['rating'],
                'tasting_date': result['tasting_date']
            })
            results = self.db.fetch_all()
            for row in results:
                wine['tastings'].append({
                    'author': row['author'],
                    'notes': row['notes'],
                    'rating': row['rating'],
                    'tasting_date': row['tasting_date']
                })
        return wine

    def get_authors(self):
        self.db.execute(self.authors_query)
        return self.db.fetch_all()

    # returns a vector of ids
    def get_author_ids(self):
        self.db.execute(self.author_ids_query)
        results = self.db.fetch_all()
        ids = []
        for row in results:
            ids.append(row['id'])
        return ids

    def get_author_page(self, pagenum=1):
        pageparams = self.page_size, self.page_size * (pagenum - 1)
        self.db.execute(self.author_page_query.format(*pageparams))
        return self.db.fetch_all()

    def get_num_author_pages(self):
        self.db.execute(self.author_count_query)
        result = self.db.fetch_one()
        count = float( result['count'] );
        return int( math.ceil( count / self.page_size ) )

    def get_author(self, authorid):
        self.db.execute(self.author_query.format(authorid))
        result = self.db.fetch_one()
        if result is None: return {}
        author = {
            'name': result['name'],
            'tastings': []
        }
        if result['wine'] is not None:
            author['tastings'].append({
                'wine': result['wine'],
                'notes': result['notes'],
                'rating': result['rating']
            })
            results = self.db.fetch_all()
            for row in results:
                author['tastings'].append({
                    'wine': row['wine'],
                    'notes': row['notes'],
                    'rating': row['rating']
                })
        return author

