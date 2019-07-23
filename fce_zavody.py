import psycopg2
import psycopg2.extras
import os
from flask import g



def get_db():
    """ Spojeni s dtb. """

    if not hasattr(g, 'db') or g.db.closed == 1:
		# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
    #database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require', cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = con
    return g.db

def zavody_dle_datumu(datum_zavodu):
    """ Vypise seznam zavodu dle vybraneho datumu v klesajicim poradi. """

    sql = """SELECT * FROM zavody WHERE datum_zavodu = %s ORDER BY datum_zavodu DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, (datum_zavodu,))
    data = cur.fetchall()
    return data


# Zaregistruje funkci show_about() jako funkci, kterou má Flask zavolat, když 
# uživatel otevře v prohlížeči stránku "/zavody"