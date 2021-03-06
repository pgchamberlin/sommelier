#!python
import math
from dbconnector import SommelierDbConnector

class SommelierBroker:

    tastings_query = """
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
        SELECT a.*, t.*, w.name as wine, w.vintage FROM author a
        JOIN tasting t ON t.author_id = a.id
        JOIN wine w ON t.wine_id = w.id
        WHERE a.id = {}
        """
    author_count_query = """
        SELECT COUNT(*) AS count FROM author a
        """
    # scalability issues w/ multiple sub-queries ?
    comparable_author_tastings_query = """
        SELECT t.*, a.*
        FROM tasting t
        JOIN author a ON t.author_id = a.id
        WHERE t.author_id <> 0
        AND t.author_id IN (
            SELECT DISTINCT t2.author_id
            FROM tasting t2
            WHERE t2.wine_id IN ( 
                SELECT t3.wine_id 
                FROM tasting t3 
                WHERE t3.author_id = {}
            )
        )
        ORDER BY t.author_id ASC, t.wine_id ASC
    """
    # scalability issues w/ multiple sub-queries ?
    comparable_wine_tastings_query = """
        SELECT t.*, a.*
        FROM tasting t
        JOIN author a ON t.author_id = a.id
        AND t.wine_id IN (
            SELECT DISTINCT t2.wine_id
            FROM tasting t2
            WHERE t2.author_id IN ( 
                SELECT t3.author_id 
                FROM tasting t3 
                WHERE t3.wine_id = {}
            )
        )
        ORDER BY t.wine_id ASC, t.author_id ASC
    """
    page_size = 50

    def __init__(self, db=SommelierDbConnector()):
        self.db = db
    
    def get_tastings(self):
        self.db.execute(self.tastings_query)
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
            'id': result['id'],
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
        if result['rating'] is not None:
            wine['tastings'].append({
                'author_id': result['author_id'],
                'author': result['author'],
                'notes': result['notes'],
                'rating': result['rating'],
                'tasting_date': result['tasting_date']
            })
            results = self.db.fetch_all()
            for row in results:
                wine['tastings'].append({
                    'author_id': row['author_id'],
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
            'id': result['author_id'],
            'tastings': []
        }
        if result['wine'] is not None:
            author['tastings'].append({
                'wine_id': result['wine_id'],
                'wine': result['wine'],
                'vintage': result['vintage'],
                'notes': result['notes'],
                'tasting_date': result['tasting_date'],
                'rating': result['rating']
            })
            results = self.db.fetch_all()
            for row in results:
                author['tastings'].append({
                    'wine_id': row['wine_id'],
                    'wine': row['wine'],
                    'vintage': row['vintage'],
                    'notes': row['notes'],
                    'tasting_date': row['tasting_date'],
                    'rating': row['rating']
                })
        return author

    def get_comparable_author_tastings(self, author_id):
        self.db.execute(self.comparable_author_tastings_query.format(author_id))
        results = self.db.fetch_all()
        return results

    def get_comparable_wine_tastings(self, wine_id):
        self.db.execute(self.comparable_wine_tastings_query.format(wine_id))
        results = self.db.fetch_all()
        return results

