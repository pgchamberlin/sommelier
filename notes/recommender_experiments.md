# Experiments

Data set: all wines with complete data and > 1 named author tasting

    select sw.name, sw.vintage, t.author, t.rating, t.notes from sommelier_wine_complete sw join sommelier_tasting t on t.wine_id = sw.id where 1 < ( select count( distinct t2.author ) from sommelier_tasting t2 where t2.wine_id = sw.id and t.rating <> 0 )

Contains:

 - 7 authors
 - 65 wines
 - 2 countries (Fr, It) - only 2! 
 - 3 regions
 - 6 sub-regions

So not very much data!

Matrix sparsity:

 - 58 wines tasted by two distinct authors
 - 7 wines tasted by three distinct authors
 - No wine tasted by > 3 distinct authors

Python console:

    # load wines from sommelier db
    from lib import recommendations
    wines = recommendations.loadSommelierWines()

    # using methods from Segaran get similar items
    winesim = recommendations.calculateSimilarItems(wines)


