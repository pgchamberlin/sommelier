#!text

# SQL Queries / Data cleanup (notes)

## Modification of tasting notes database

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
Wine data completeness...

    SELECT COUNT(*) FROM sommelier WHERE (grape_variety IS NULL OR appellation IS NULL OR sub_region IS NULL OR region IS NULL OR country IS NULL OR producer IS NULL OR type IS NULL OR style IS NULL OR colour IS NULL);
    +----------+
    | COUNT(*) |
    +----------+
    |    21516 |
    +----------+
    1 row in set (0.04 sec)


    SELECT COUNT(*) FROM sommelier WHERE (grape_variety IS NULL OR appellation IS NULL OR sub_region IS NULL OR region IS NULL OR country IS NULL OR producer IS NULL);
    +----------+
    | COUNT(*) |
    +----------+
    |    14830 |
    +----------+
    1 row in set (0.00 sec)

    SELECT COUNT(*) FROM sommelier WHERE (grape_variety IS NULL OR appellation IS NULL);
    +----------+
    | COUNT(*) |
    +----------+
    |    14222 |
    +----------+
    1 row in set (0.00 sec)

    mysql> SELECT COUNT(*) FROM sommelier WHERE (grape_variety IS NULL);
    +----------+
    | COUNT(*) |
    +----------+
    |    13523 |
    +----------+
    1 row in set (0.00 sec)

    mysql> SELECT COUNT(*) FROM sommelier WHERE (grape_variety IS NOT NULL AND appellation IS NOT NULL AND sub_region IS NOT NULL AND region IS NOT NULL AND country IS NOT NULL AND producer IS NOT NULL AND type IS NOT NULL AND style IS NOT NULL AND colour IS NOT NULL );
    +----------+
    | COUNT(*) |
    +----------+
    |    10169 |
    +----------+
    1 row in set (0.05 sec)

## Conversion from latin1 to utf8:

Based on advice from: http://en.gentoo-wiki.com/wiki/Convert_latin1_to_UTF-8_in_MySQL

    From the Bash shell:
    $ mysqldump -uroot -p -hlocalhost --default-character-set=latin1 -c --insert-ignore --skip-set-charset -r wine_dump.sql wine
    $ file wine_dump.sql
    > wine_dump.sql: Non-ISO extended-ASCII English text, with very long lines
    $ iconv -f ISO8859-1 -t UTF-8 wine_dump.sql > wine_dump_utf8.sql
    $ sed -i 's/latin1/utf8/g' wine_dump_utf8.sql

    Now, from the MySQL command line:
    mysql> CREATE DATABASE sommelier CHARACTER SET utf8 COLLATE utf8_general_ci;

    And finally, back in the Bash shell:
    $ mysql -uroot --max_allowed_packet=16M -p --default-character-set=utf8 sommelier < wine_dump_utf8.sql

-----------------------------------------------------

mysql> select count(*) from tasting t join wine w on w.id = t.wine_id join wine_info wi on w.id = wi.id left join producers p on p.id = wi.producer_id left join wine_grape_variety gv on gv.id = wi.grape_variety where t.rating > 0 and t.notes <> '' and w.vintage > 1900 and w.vintage < 2013 and wi.appellation_id <> 0 order by rand() limit 2\G
*************************** 1. row ***************************
count(*): 14273
1 row in set (0.20 sec)

--------------------------------------------------------

Content for sommelier.wine:

CREATE TABLE `sommelier_wine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `vintage` int(4) NOT NULL DEFAULT '0',
  `grape_variety` varchar(255) NOT NULL DEFAULT '',
  `producer` varchar(255) NOT NULL DEFAULT '',
  `country` varchar(255) NOT NULL DEFAULT '',
  `region` varchar(255) NOT NULL DEFAULT '',
  `sub_region` varchar(255) NOT NULL DEFAULT '',
  `appellation` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO sommelier_wine SELECT 
  w.id,
  w.name AS name, 
  w.vintage AS vintage, 
  p.producer_match AS producer, 
  gv.description AS description,
  c.country AS country,
  r.region AS region,
  sr.sub_region AS sub_region,
  a.appellation AS appellation
FROM
  wine w 
JOIN wine_info wi ON w.id = wi.id 
LEFT JOIN producers p ON p.id = wi.producer_id 
LEFT JOIN wine_grape_variety gv ON gv.id = wi.grape_variety 
LEFT JOIN appellation a ON a.id = wi.appellation_id
LEFT JOIN sub_region sr ON sr.id = a.sub_region_id
LEFT JOIN region r ON r.id = sr.region_id
LEFT JOIN country c ON c.id = r.country_id
ORDER BY w.id ASC;

Content for sommelier.author:

CREATE TABLE `sommelier_author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO sommelier_author SELECT DISTINCT
  NULL,
  t.author as name
FROM
  tasting t
WHERE t.author <> '';

Content for sommelier.tasting:

CREATE TABLE `sommelier_tasting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wine_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `notes` TEXT NOT NULL,
  `tasting_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `wine_idx` (`wine_id`),
  KEY `author_idx` (`author_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO sommelier_tasting SELECT
  NULL,
  t.wine_id AS wine_id,
  a.id AS author_id,
  t.rating AS rating,
  t.notes AS notes,
  t.tasting_date AS tasting_date
FROM
  tasting t 
JOIN wine w ON w.id = t.wine_id 
JOIN wine_info wi ON w.id = wi.id 
LEFT JOIN sommelier_author a ON t.author = a.name
WHERE t.rating > 0 
  AND t.notes <> '' 
ORDER BY w.id ASC;

Finally, delete all wines without tasting records:

DELETE FROM sommelier_wine WHERE id NOT IN ( SELECT wine_id FROM sommelier_tasting );

DROP TABLE wine;
DROP TABLE tasting;
DROP TABLE author;

RENAME TABLE sommelier_wine TO wine;

RENAME TABLE sommelier_tasting TO tasting;

RENAME TABLE sommelier_author TO author;

/*
mysql> show tables;
+---------------------+
| Tables_in_sommelier |
+---------------------+
| author              |
| tasting             |
| wine                |
+---------------------+
3 rows in set (0.00 sec)
*/


// Author ids...

+----+----------------------+
| id | name                 |
+----+----------------------+
|  1 | Steven Spurrier      |
|  2 | Beverley Blanning MW |
|  3 | James Lawther MW     |
|  4 | Josephine Butchart   |
|  5 | Rosemary George MW   |
|  6 | Norm Roby            |
|  7 | Clive Coates MW      |
|  8 | John Radford         |
|  9 | Gerald D Boyd        |
| 10 | Stephen Brook        |
| 11 | Christelle Guibert   |
| 12 | Alan Spencer         |
| 13 | Serena Sutcliffe     |
| 14 | Harriet Waugh        |
| 15 | Andrew Jefford       |
| 16 | David Peppercorn     |
| 17 | Richard Mayson       |
| 18 | Carolyn Holmes       |
| 19 | Amy Wislocki         |
+----+----------------------+

