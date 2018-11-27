import psycopg2
import psycopg2.extras
import os
from flask import g
from hashlib import sha512
from flask_login import UserMixin

from geopy.geocoders import Here as locator
from geopy.exc import GeopyError
from functools import lru_cache

class User(UserMixin):
    def __init__(self, id, db_id, password_hash, jmeno, prijmeni):
        self.id = id  # id-čkem je pro nás email uživatele
        self.db_id = db_id
        self.password_hash = password_hash
        self.jmeno = jmeno
        self.prijmeni = prijmeni


def get_db():
    """ Spojeni s dtb. """

    if not hasattr(g, 'db') or g.db.closed == 1:
		# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
    #database_url = os.environ["DATABASE_URL"]
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
    """ Hashovani hesel do dtb pri registraci noveho uzivatele. """

    return sha512(heslo.encode()).hexdigest()


def get_gps(ulice, PSC):
    """ Ziska GPS souradnice z Here map."""

    app_id = 'LJYFl2AZbHtLHftkJeWA'
    app_code = 'C7sHEhOBFLTVZCQ2K8S4-A'

    connection = locator(app_id=app_id, app_code=app_code)

    query = '{}, {}, czech republic'.format(ulice, PSC)
    try:
        data = connection.geocode(query)
    except GeopyError:
        return (.0, .0)
    return (.0, .0) if data is None else (data.latitude, data.longitude)


def registrace(jmeno, prijmeni, ulice, mesto, psc, email, telefon, heslo, heslo_potvrzeni):
    """ vlozi noveho uzivatele do databaze """

    sql = """INSERT INTO uzivatele
            (jmeno, prijmeni, ulice, mesto_obec, "PSC", email, telefon, heslo, latitude, longitude)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_uzivatele;"""
    conn = get_db()
    id_uzivatele = None
    latitude, longitude = get_gps(ulice, psc)
    heslo = hash_heslo(heslo)

    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (jmeno, prijmeni, ulice, mesto, psc, email, telefon, heslo, latitude, longitude))
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
    return id_uzivatele


def najdi_uzivatele(email):
    """ najde uzivatele v databazi """

    sql = """SELECT id_uzivatele, jmeno, prijmeni, email, heslo FROM uzivatele WHERE lower(email)=%s;"""
    conn = get_db()

    uzivatel = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (email.lower(),))
        # get the generated id back
        uzivatel = cur.fetchone()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if uzivatel:
        return User(uzivatel[3], uzivatel[0], uzivatel[4], uzivatel[1], uzivatel[2])
    else:
        return None


def nove_auto(ridic, id_zavod, misto_odjezdu, datum_odjezdu, mist_auto_nabidka, poznamky):
    """ prida nove auto s ridicem do databaze """

    sql_najdi_auto = """SELECT * from nabidka_spolujizdy WHERE ridic = %s and id_zavod = %s;"""

    sql_zapis_auto = """INSERT INTO nabidka_spolujizdy(ridic, id_zavod, misto_odjezdu, datum_odjezdu, mist_auto_nabidka, poznamky)
             VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_jizdy; """

    conn = get_db()
    id_jizdy = None
    
    try:
        cur = conn.cursor()
        cur.execute(sql_najdi_auto, (ridic, id_zavod))
        # execute the SELECT statement
        vysledek = cur.fetchall()
        if vysledek:
            return None
        # execute the INSERT statement
        cur.execute(sql_zapis_auto, (ridic, id_zavod, misto_odjezdu, datum_odjezdu, mist_auto_nabidka, poznamky))
        # get the generated id back
        id_jizdy = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id_jizdy


def nabidky_spolujizdy(id_zavodu):
    """ nabidne volna auta ke konkretnimu zavodu """
    
    sql = """SELECT ns.id_jizdy, jmeno, misto_odjezdu, datum_odjezdu, (mist_auto_nabidka - coalesce(sum_obsazena_mista, 0)) as
    volnych_mist, poznamky FROM
    nabidka_spolujizdy as ns 
    left join 
        (select id_jizdy, sum(chci_mist) as sum_obsazena_mista from 
        spolujezdci as s 
        group by s.id_jizdy) as s
    on ns.id_jizdy = s.id_jizdy
    left join
		(select jmeno, id_uzivatele from
		 uzivatele as u) as u
	on ns.ridic = u.id_uzivatele
     where (mist_auto_nabidka > sum_obsazena_mista or s.id_jizdy is null) AND id_zavod=%s
     order by misto_odjezdu;
     """
    conn = get_db()
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


def vyber_spolujizdu(id_jizdy):
    """ Vybere konkretni id jizdy pro spolujizdu """

    sql = """SELECT ns.id_jizdy, jmeno, misto_odjezdu, datum_odjezdu, (mist_auto_nabidka - coalesce(sum_obsazena_mista, 0)) as
    volnych_mist, poznamky FROM
    nabidka_spolujizdy as ns 
    left join 
        (select id_jizdy, sum(chci_mist) as sum_obsazena_mista from 
        spolujezdci as s 
        group by s.id_jizdy) as s
    on ns.id_jizdy = s.id_jizdy
    left join
		(select jmeno, id_uzivatele from
		 uzivatele as u) as u
	on ns.ridic = u.id_uzivatele
            WHERE ns.id_jizdy=%s;"""

    conn = get_db()
    try:
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql, (id_jizdy,))
        # close communication with the database
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def chci_nastoupit(id_jizdy, spolujezdec, chci_mist):
    """ vlozi spolujezdce do db """

    sql_zjisti = """SELECT * FROM spolujezdci
                   WHERE id_jizdy = %s
                   AND spolujezdec = %s"""

    sql_zapis = """INSERT INTO spolujezdci(id_jizdy, spolujezdec, chci_mist)
                        VALUES(%s, %s, %s);"""


    conn = get_db()

    try:
        cur = conn.cursor()
        cur.execute(sql_zjisti, (id_jizdy, spolujezdec))
        # execute the SELECT statement
        vysledek = cur.fetchall()
        if vysledek:
            return vysledek[0].id_jizdy
        cur.execute(sql_zapis, (id_jizdy, spolujezdec, chci_mist))
        conn.commit()
        # close communication with the database
        # return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def potvrzeni_spolujizdy(id_jizdy, spolujezdec):
    """ Najde jizdu podle id_jizdy a spolujezdce """

    sql = """SELECT ns.id_jizdy, jmeno, misto_odjezdu, datum_odjezdu, chci_mist, spolujezdec, poznamky FROM
    nabidka_spolujizdy as ns 
    left join 
        (select id_jizdy, spolujezdec, chci_mist from 
        spolujezdci as s) as s
    on ns.id_jizdy = s.id_jizdy
    left join
		(select jmeno, id_uzivatele from
		 uzivatele as u) as u
	on ns.ridic = u.id_uzivatele
            WHERE ns.id_jizdy=%s and spolujezdec=%s;"""

    conn = get_db()
    try:
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql, (id_jizdy, spolujezdec))
        # close communication with the database
        return cur.fetchone()
        # print(cur.fetchone())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

'''
if __name__ == '__main__':
    print(get_gps('Otokara Breziny 1109', 25082))
'''