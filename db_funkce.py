import psycopg2
import psycopg2.extras
import os
from flask import g


def get_db():
    if not hasattr(g, 'db'):
        # https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require', cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = con
    return g.db


def zavody():
    sql = """SELECT * FROM zavody ORDER BY datum_zavodu DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data


def registrace(jmeno, prijmeni, ulice, mesto_obec, PSC, email, telefon, heslo):
    """ vlozi noveho uzivatele do databaze """
    sql = """INSERT INTO uzivatele(jmeno, prijmeni, ulice, mesto_obec, PSC, email, telefon, heslo)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_uzivatele;"""
    conn = get_db()
    id_uzivatele = None
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (jmeno, prijmeni, ulice, mesto_obec, PSC, email, telefon, heslo))
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
    sql = """SELECT ridic, misto_odjezdu, datum_odjezdu, (mist_auto_nabidka - sum(chci_mist) as
    volnych_mist FROM
    (select * from 
    nabidka_spolujizdy as ns left join spolujezdci as s on ns.id_jizdy = s.id_jizdy
    group by ns.id_jizdy)
     where mist_auto_nabidka > sum(chci_mist)
     order by misto_odjezdu
     """
    conn = get_db()
    id_uzivatele = None
    try:
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql, (id_zavodu))
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()