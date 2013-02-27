# SQL Queries / Data (notes)

Modification of tasting notes database

update tasting set author = 'Christelle Guibert' where author = 'C hristelle Guibert';

update tasting set author = '' where author in ('Rising stars','New releases','Great wine buys','Panel Tasting','Hot tip','Wine of the month','Wine of the week','Connoisseur\'s choice','Decanter choice','Decanter Fine Wine Encounter 2002','In the Decanter tasting room','Christmas choice','') or author is NULL;

Select count of wines tasted by each taster in author column of `tasting`:

Tasting dates:
>
>  With date: 15006
>  0000-00-00 00:00:00: 24595
>
>mysql> select t.author, count(*) from tasting as t join wine as w on t.wine_id = w.id where author is not NULL and author <> '' and author not in ('Rising stars','New releases','Great wine buys','Panel Tasting','Hot tip','Wine of the month','Wine of the week','Connoisseur\'s choice','Decanter choice','Decanter Fine Wine Encounter 2002','In the Decanter tasting room','Christmas choice') group by t.author;
>+----------------------+----------+
>| author               | count(*) |
>+----------------------+----------+
>| Alan Spencer         |       19 |
>| Amy Wislocki         |       29 |
>| Andrew Jefford       |      105 |
>| Beverley Blanning MW |       13 |
>| Carolyn Holmes       |        1 |
>| Christelle Guibert   |      120 |
>| Clive Coates MW      |        6 |
>| David Peppercorn     |       45 |
>| Gerald D Boyd        |        7 |
>| Harriet Waugh        |      253 |
>| James Lawther MW     |      238 |
>| John Radford         |        2 |
>| Josephine Butchart   |       24 |
>| Norm Roby            |        4 |
>| Richard Mayson       |       14 |
>| Rosemary George MW   |        6 |
>| Serena Sutcliffe     |       31 |
>| Stephen Brook        |      491 |
>| Steven Spurrier      |      510 |
>+----------------------+----------+
>19 rows in set (0.03 sec)
>
>Investigation of prices in tasting notes:
>
>select price from tasting where price not like '£%' and price not like '$%' and price != '' and price is not null and price not like 'n/a%' and price not like 'POA' and price not like '%TBC%' and price not like 'na%' and price not like 'Nicholas' and price not like '%old out%' and price not like 'n./a%' and price not like 'tcb%' and price not like 'n/ a%' and price not like '%request%' and price not like '%poa%' and price not like '%Howard Ripley%' and price not like '%N\'/A%' and price not like 'N/A' and price not like '%ut of%' and price not like '%tba%' and price not like '%trade%' and price not like '%undefined%' and price not like '%unreleased%';
>
