#!python
from sommelier import SommelierDb, SommelierBroker
import math

class WineBroker(SommelierBroker):

    winesquerycomplete = """
        SELECT * 
        FROM sommelier_wine_complete
        WHERE (grape_variety IS NOT NULL AND appellation IS NOT NULL AND sub_region IS NOT NULL AND region IS NOT NULL AND country IS NOT NULL AND producer IS NOT NULL AND type IS NOT NULL AND style IS NOT NULL AND colour IS NOT NULL )
        LIMIT {} OFFSET {}"""
    winequerycomplete  = """
        SELECT * FROM sommelier_wine_complete s 
        LEFT JOIN sommelier_tasting t ON s.id = t.wine_id 
            AND t.author <> ''
        WHERE s.id = {}
        AND (grape_variety IS NOT NULL AND appellation IS NOT NULL AND sub_region IS NOT NULL AND region IS NOT NULL AND country IS NOT NULL AND producer IS NOT NULL AND type IS NOT NULL AND style IS NOT NULL AND colour IS NOT NULL )
    """
    countquerycomplete = """
        SELECT COUNT(*) FROM sommelier_wine_complete
        WHERE (grape_variety IS NOT NULL AND appellation IS NOT NULL AND sub_region IS NOT NULL AND region IS NOT NULL AND country IS NOT NULL AND producer IS NOT NULL AND type IS NOT NULL AND style IS NOT NULL AND colour IS NOT NULL )
        """
    winesquery = """
        SELECT * 
        FROM sommelier_wine
        WHERE (grape_variety IS NOT NULL AND appellation IS NOT NULL AND sub_region IS NOT NULL AND region IS NOT NULL AND country IS NOT NULL AND producer IS NOT NULL AND type IS NOT NULL AND style IS NOT NULL AND colour IS NOT NULL )
        LIMIT {} OFFSET {}"""
    winequery  = """
        SELECT * FROM sommelier_wine s 
        LEFT JOIN tasting t ON s.id = t.wine_id 
            /* AND t.author <> '' */
        WHERE s.id = {}
        AND (grape_variety IS NOT NULL AND appellation IS NOT NULL AND sub_region IS NOT NULL AND region IS NOT NULL AND country IS NOT NULL AND producer IS NOT NULL AND type IS NOT NULL AND style IS NOT NULL AND colour IS NOT NULL )
    """
    countquery = """
        SELECT COUNT(*) FROM sommelier_wine
        WHERE (grape_variety IS NOT NULL AND appellation IS NOT NULL AND sub_region IS NOT NULL AND region IS NOT NULL AND country IS NOT NULL AND producer IS NOT NULL AND type IS NOT NULL AND style IS NOT NULL AND colour IS NOT NULL )
        """
    pagesize = 50

    def __init__(self, db=SommelierDb()):
        self.db = db

    def getPage(self, pagenum=1):
        pageparams = self.pagesize, self.pagesize * (pagenum - 1)
        self.db.execute(self.winesquerycomplete.format(*pageparams))
        return self.db.fetchall()

    def getNumPages(self):
        self.db.execute(self.countquerycomplete)
        result = self.db.fetchone()
        count = float( result['COUNT(*)'] );
        return int( math.ceil( count / self.pagesize ) )

    def getWine(self, wineid):
        self.db.execute(self.winequerycomplete.format(wineid))
        result = self.db.fetchone()
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
                'type': result['type'],
                'style': result['style'],
                'colour': result['colour'],
                'tastings': [
                ]
            }
        if result['author'] is not None:
            wine['tastings'].append(
                    {
                    'author': result['author'],
                    'notes': result['notes'],
                    'rating': result['rating'],
                    'tasting_date': result['tasting_date']
                    }
            )
        results = self.db.fetchall()
        for row in results:
            wine['tastings'].append(
                    {
                    'author': row['author'],
                    'notes': row['notes'],
                    'rating': row['rating'],
                    'tasting_date': row['tasting_date']
                    }
                )
        return wine

