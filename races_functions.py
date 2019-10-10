import psycopg2
import psycopg2.extras
import os
from flask import g


def get_db():
    """ Connection with database. """

    if not hasattr(g, 'db') or g.db.closed == 1:
        # https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
    #database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require', cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = con
    return g.db


def races_for_date(date_race):
    """ Returns list of get_races according to the selected date in decreasing order. """

    sql = """SELECT * FROM zavody WHERE datum_zavodu = %s ORDER BY datum_zavodu DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, (date_race,))
    data = cur.fetchall()
    return data