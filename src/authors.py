#!python
import math
from sommelier import Sommelier, SommelierDb

class AuthorBroker():

    authors_query = """
        SELECT * 
        FROM author a
        """
    authors_page_query = """
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
    authors_count_query = """
        SELECT COUNT(*) AS count FROM author a
        """
    page_size = 50

    def __init__(self, db=SommelierDb(), sommelier=Sommelier()):
        self.db = db
        self.sommelier = sommelier

    def get_page(self, pagenum=1):
        pageparams = self.page_size, self.page_size * (pagenum - 1)
        self.db.execute(self.authors_page_query.format(*pageparams))
        return self.db.fetch_all()

    def get_num_pages(self):
        self.db.execute(self.authors_count_query)
        result = self.db.fetch_one()
        count = float( result['count'] );
        return int( math.ceil( count / self.page_size ) )

    def get_author(self, authorid):
        self.db.execute(self.author_query.format(authorid))
        result = self.db.fetch_one()
        if result is None: return {}
        recommendations = self.sommelier.get_recommended_wines('author', authorid)
        author = {
            'name': result['name'],
            'tastings': [],
            'recommendations': recommendations
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


