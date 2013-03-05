# Using MySQLdb

Using MySQLdb:

    import MySQLdb
    from MySQLdb.constants import FIELD_TYPE
    from MySQLdb.cursors import DictCursor
    converter={ FIELD_TYPE.LONG: int }
    db=MySQLdb.connect(user="sommelier",db="wine",passwd="vinorosso",conv=converter)
    c=db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM sommelier")

Using MySQLdb to get records in dictionary for 'recommendations' use:

    >>> import recommendations
    >>> import MySQLdb
    >>> from MySQLdb.constants import FIELD_TYPE
    >>> from MySQLdb.cursors import DictCursor
    >>> converter={ FIELD_TYPE.LONG: int }
    >>> db=MySQLdb.connect(user="sommelier",db="wine",passwd="vinorosso",conv=converter)
    >>> c=db.cursor(MySQLdb.cursors.DictCursor)
    >>> c.execute("SELECT * FROM sommelier")
