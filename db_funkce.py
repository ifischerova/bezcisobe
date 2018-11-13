import psycopg2
import psycopg2.extras
import os
from flask import g
from hashlib import sha512

from geopy.geocoders import Here as locator
from geopy.exc import GeopyError
from functools import lru_cache



def get_db():
    """ Spojeni s dtb. """

    if not hasattr(g, 'db'):
        # https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require', cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = con
    return g.db


def zavody():
    """ Vypise seznam zavodu na webu v klesajicim poradi. """

    sql = """SELECT * FROM zavody ORDER BY datum_zavodu DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data


def hash_heslo(heslo):
    """ Hashovani hesel do dtb pri regostraci noveho uzivatele. """

    return sha512(b'heslo').hexdigest()


@lru_cache(maxsize=None)
def get_gps(ulice, PSC):
    """ Ziska GPS souradnice z Here map."""

    app_id = 'LJYFl2AZbHtLHftkJeWA'
    app_code = 'C7sHEhOBFLTVZCQ2K8S4-A'

    connection = locator(app_id=app_id, app_code=app_code)

    query = '{}, {}, czech republic'.format(ulice, PSC)
    try:
        data = connection.geocode(query)
    except GeopyError:
        return ('', '')
    return data.latitude, data.longitude


def registrace(jmeno, prijmeni, ulice, mesto_obec, PSC, email, telefon, heslo):
    """ vlozi noveho uzivatele do databaze """

    sql = """INSERT INTO uzivatele
            (jmeno, prijmeni, ulice, mesto_obec, PSC, latitude, longitude, email, telefon, heslo)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_uzivatele;"""
    conn = get_db()
    id_uzivatele = None
    latitude, longitude = get_gps(ulice, PSC)

    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (jmeno, prijmeni, ulice, mesto_obec, PSC, latitude, longitude, email, telefon, hash_heslo(heslo)))
        # get the generated id back
        id_uzivatele = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def nove_auto(ridic, id_zavod, misto_odjezdu, datum_odjezdu, mist_auto_nabidka):
    """ prida nove auto s ridicem do databaze """

    sql = """INSERT INTO nabidka_spolujizdy(ridic, id_zavod, misto_odjezdu, datum_odjezdu, mist_auto_nabidka)
             VALUES(%s, %s, %s, %s, %s) RETURNING id_jizdy;"""
    conn = get_db()
    id_uzivatele = None
    
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (ridic, id_zavod, misto_odjezdu, datum_odjezdu, mist_auto_nabidka))
        # get the generated id back
        id_spolujizdy = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def nabidky_spolujizdy(id_zavodu):
    """ nabidne volna auta ke konkretnimu zavodu """
    
    sql = """SELECT ridic, misto_odjezdu, datum_odjezdu, (mist_auto_nabidka - coalesce(sum_obsazena_mista, 0)) as
    volnych_mist FROM
    nabidka_spolujizdy as ns 
    left join 
        (select id_jizdy, sum(chci_mist) as sum_obsazena_mista from 
        spolujezdci as s 
        group by s.id_jizdy) as s
    on ns.id_jizdy = s.id_jizdy
     where (mist_auto_nabidka > sum_obsazena_mista or s.id_jizdy is null) AND id_zavod=%s
     order by misto_odjezdu;
     """
    conn = get_db()
    id_jizdy = None
    try:
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql, (id_zavodu,))
        # close communication with the database
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

'''
if __name__ == '__main__':
    print(get_gps('Otokara Breziny 1109', 25082))
'''