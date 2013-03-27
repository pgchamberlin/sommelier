# Data analysis stats / queries appendix

mysql> select vintage, count(*) from sommelier_wine s join tasting t on s.id = t.wine_id where t.rating > 0 and t.notes <> '' and s.vintage > 1900 and s.vintage < 2013 group by vintage;
+---------+----------+
| vintage | count(*) |
+---------+----------+
|    1917 |        1 |
|    1928 |        1 |
|    1939 |        1 |
|    1947 |        1 |
|    1949 |        1 |
|    1953 |        1 |
|    1959 |        1 |
|    1961 |        2 |
|    1962 |        1 |
|    1964 |        4 |
|    1966 |        4 |
|    1967 |        1 |
|    1968 |        1 |
|    1970 |        4 |
|    1971 |        3 |
|    1973 |        3 |
|    1976 |        3 |
|    1978 |        2 |
|    1979 |        3 |
|    1980 |        1 |
|    1981 |        3 |
|    1982 |       27 |
|    1983 |       52 |
|    1984 |        6 |
|    1985 |      100 |
|    1986 |       60 |
|    1987 |       18 |
|    1988 |       90 |
|    1989 |      124 |
|    1990 |      307 |
|    1991 |       73 |
|    1992 |      123 |
|    1993 |      250 |
|    1994 |      375 |
|    1995 |      957 |
|    1996 |      873 |
|    1997 |      920 |
|    1998 |      807 |
|    1999 |     1251 |
|    2000 |     2025 |
|    2001 |     1996 |
|    2002 |     1185 |
|    2003 |     1544 |
|    2004 |     2454 |
|    2005 |     2392 |
|    2006 |     1689 |
|    2007 |     2065 |
|    2008 |     1724 |
|    2009 |     1689 |
|    2010 |     1007 |
|    2011 |      370 |
+---------+----------+
51 rows in set (0.12 sec)

# Wines to work with:

mysql> select count(*) from recommendations_group rg join recommendations r on r.recommend_group = rg.id join tasting t on t.recommend_id = r.id left join taster_name tn on tn.recommend_id = r.id left join taster_rating tr on tr.tasting_id = t.id;
+----------+
| count(*) |
+----------+
|    28709 |
+----------+
1 row in set (0.00 sec)

