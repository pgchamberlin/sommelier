#!python
from sommelier import Sommelier, SommelierDb

class WineBroker():

    winesquery = """
        SELECT * 
        FROM wine w
        LIMIT {} OFFSET {}
        """
    winequery  = """
        SELECT w.*, t.*, a.name AS author FROM wine w
        LEFT JOIN tasting t ON w.id = t.wine_id 
        LEFT JOIN author a ON t.author_id = a.id
        WHERE w.id = {}
        """
    countquery = """
        SELECT COUNT(*) AS count FROM wine
        """
    pagesize = 50

    def __init__(self, db=SommelierDb(), sommelier=Sommelier()):
        self.db = db
        self.sommelier = sommelier

    def get_page(self, pagenum=1):
        pageparams = self.pagesize, self.pagesize * (pagenum - 1)
        self.db.execute(self.winesquery.format(*pageparams))
        return self.db.fetch_all()

    def get_num_pages(self):
        self.db.execute(self.countquery)
        result = self.db.fetch_one()
        count = float( result['count'] );
        return int( math.ceil( count / self.pagesize ) )

    def get_wine(self, wineid):
        self.db.execute(self.winequery.format(wineid))
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
            'tastings': [],
            'recommendations': self.sommelier.get_recommended_wines('wine', wineid)
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

