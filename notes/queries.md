# SQL Queries / Data (notes)

Modification of tasting notes database

    update tasting set author = 'Christelle Guibert' where author = 'C hristelle Guibert';

    update tasting set author = '' 
      where author in (
        'Rising stars',
        'New releases',
        'Great wine buys',
        'Panel Tasting',
        'Hot tip',
        'Wine of the month',
        'Wine of the week',
        'Connoisseur\'s choice',
        'Decanter choice',
        'Decanter Fine Wine Encounter 2002',
        'In the Decanter tasting room',
        'Christmas choice',
        ''
      )
      or author is NULL;


Number of tasting notes with date: 15006

Number of tasting notes without date (0000-00-00 00:00:00): 24595

Select count of wines tasted by each taster in author column of \`tasting\`:

    select t.author, count(*) 
    from tasting as t 
    join wine as w on t.wine_id = w.id 
    where author is not NULL 
      and author <> '' 
      and author not in (
        'Rising stars',
        'New releases',
        'Great wine buys',
        'Panel Tasting',
        'Hot tip',
        'Wine of the month',
        'Wine of the week',
        'Connoisseur\'s choice',
        'Decanter choice',
        'Decanter Fine Wine Encounter 2002',
        'In the Decanter tasting room',
        'Christmas choice'
      ) 
      group by t.author;

    +----------------------+----------+
    | author               | count(*) |
    +----------------------+----------+
    | Alan Spencer         |       19 |
    | Amy Wislocki         |       29 |
    | Andrew Jefford       |      105 |
    | Beverley Blanning MW |       13 |
    | Carolyn Holmes       |        1 |
    | Christelle Guibert   |      120 |
    | Clive Coates MW      |        6 |
    | David Peppercorn     |       45 |
    | Gerald D Boyd        |        7 |
    | Harriet Waugh        |      253 |
    | James Lawther MW     |      238 |
    | John Radford         |        2 |
    | Josephine Butchart   |       24 |
    | Norm Roby            |        4 |
    | Richard Mayson       |       14 |
    | Rosemary George MW   |        6 |
    | Serena Sutcliffe     |       31 |
    | Stephen Brook        |      491 |
    | Steven Spurrier      |      510 |
    +----------------------+----------+
    19 rows in set (0.03 sec)

Investigation of prices in tasting notes:

    select price from tasting 
    where price not like '£%' 
      and price not like '$%' 
      and price != '' 
      and price is not null 
      and price not like 'n/a%' 
      and price not like 'POA' 
      and price not like '%TBC%' 
      and price not like 'na%' 
      and price not like '%Nicholas%' 
      and price not like '%old out%' 
      and price not like 'n./a%' 
      and price not like 'tcb%' 
      and price not like 'n/ a%' 
      and price not like '%request%' 
      and price not like '%poa%' 
      and price not like '%Howard Ripley%' 
      and price not like '%N\'/A%' 
      and price not like '%N/A%' 
      and price not like '%ut of%' 
      and price not like '%tba%' 
      and price not like '%trade%' 
      and price not like '%undefined%' 
      and price not like '%unreleased%'
      and price not like '%N/UK%'
      and price not like '%not released%'
      and price not like '%limited avail%'
      and price not like '%on reques%'
      and price not like '%not in st%'
      and price not like '%ice on ap%'
      and price not like '%JkN%'
      and price not like '%autumn%'
      and price not like '%#316'
      and price not like '%not ye%'
      and price not like '%Lib%';

How many wines are there which have been tasted by > 1 named author?

    mysql> select count(*) from wine w where 1 < ( select count(*) from tasting t2 where t2.author <> '' and t2.wine_id = w.id);
    +----------+
    | count(*) |
    +----------+
    |      104 |
    +----------+
    1 row in set (0.52 sec)

How many wines have been tasted by > 1 author, named or ''?

    mysql> select count(*) from wine w where 1 < ( select count(*) from tasting t2 where t2.wine_id = w.id);
    +----------+
    | count(*) |
    +----------+
    |     3225 |
    +----------+
    1 row in set (0.32 sec)

How many wines in total?

    mysql> select count(*) from wine;
    +----------+
    | count(*) |
    +----------+
    |    50539 |
    +----------+
    1 row in set (0.00 sec)

Generally speaking:

1918   Wines in denormalised_quick_search_data table associated with tastings with authors
1411   ... as above with rating > 0 (i.e. a valid rating)
31704  Wines in denormalised_quick_search_data with join to tasting
29185  ... as above with rating > 0
29732  ... as above with notes <> '' (i.e. written tasting note)
27232  ... as above with intersection of rating > 0 and notes <> ''`

Query for eligible wines:

    select 
      w.name, 
      w.producer, 
      w.vintage, 
      w.appellation, 
      w.sub_region, 
      w.region, 
      w.country, 
      w.wine_type, 
      w.sub_type, 
      w.colour, 
      t.notes, 
      t.author, 
      t.rating, 
      t.tasting_date, 
      t.price, 
      t.source, 
      t.status 
    from 
      denormalised_quick_search_data w 
    join tasting as t on w.id = t.wine_id 

