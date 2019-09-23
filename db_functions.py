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
    def __init__(self, id, db_id, password_hash, name, surname, phone):
        self.id = id  # email is an id for us
        self.db_id = db_id
        self.password_hash = password_hash
        self.name = name
        self.surname = surname
        self.phone = phone


def get_db():
    """ Connection with database. """

    if not hasattr(g, 'db') or g.db.closed == 1:
		# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
    #database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require', cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = con
    return g.db


def get_races():
    """ Returns list of get_races in decreasing order by date. """

    sql = """SELECT * FROM zavody ORDER BY datum_zavodu DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data


def get_race(id_race):
    """ Returns date of race, place of race and name of race in the email. """

    sql = """SELECT datum_zavodu, misto_zavodu, nazev FROM zavody WHERE id_zavod = %s"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, (id_race, ))
    data = cur.fetchone()
    return data


def get_ride_confirmation_details(id_ride):
    """ Returns name of driver, place of departure, date of departure, email and phone into an email with confirmation of the boarding to the car. """

    sql = """SELECT id_uzivatele, jmeno, telefon, email, ns.ridic, ns.misto_odjezdu, ns.datum_odjezdu, ns.id_jizdy from uzivatele as u
    left join (select ridic, misto_odjezdu, datum_odjezdu, id_jizdy from nabidka_spolujizdy as ns) as ns
    on u.id_uzivatele = ns.ridic WHERE id_jizdy= %s"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, (int(id_ride), ))
    data = cur.fetchone()
    return data


def get_ride_driver(id_ride):
    """ Returns email of driver for a email field, that is sended to the driver at moment of confirmation of the boarding to his/her offered car."""

    sql = """SELECT id_uzivatele, email, ns.ridic from uzivatele as u left join (select ns.ridic, id_jizdy from nabidka_spolujizdy as ns) as ns on ns.ridic = u.id_uzivatele WHERE id_jizdy = %s"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, (int(id_ride), ))
    data = cur.fetchone()
    return data 


def hash_password(password):
    """ Hashes passwords in database with registration of the user. """

    return sha512(password.encode()).hexdigest()


def get_gps(street, postcode):
    """ Gets GPS locators from Here maps."""

    app_id = os.environ["API_KEY_MAPS"]
    app_code = os.environ["API_CODE_MAPS"]

    connection = locator(app_id=app_id, app_code=app_code)

    query = '{}, {}, czech republic'.format(street, postcode)
    try:
        data = connection.geocode(query)
    except GeopyError:
        return (.0, .0)
    return (.0, .0) if data is None else (data.latitude, data.longitude)


def add_user(name, surname, street, city, postcode, email, phone, password, password_confirmation):
    """ Inserts new user into database. """

    sql = """INSERT INTO uzivatele
            (jmeno, prijmeni, ulice, mesto_obec, "PSC", email, telefon, heslo, latitude, longitude)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_uzivatele;"""
    conn = get_db()
    id_user = None
    latitude, longitude = get_gps(street, postcode)
    password = hash_password(password)

    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (name, surname, street, city, postcode, email, phone, password, latitude, longitude))
        # get the generated id back
        id_user = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id_user


def find_user(email):
    """ Finds user in the database. """

    sql = """SELECT id_uzivatele, jmeno, prijmeni, email, heslo, telefon FROM uzivatele WHERE lower(email)=%s;"""
    conn = get_db()

    user = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (email.lower(),))
        # get the generated id back
        user = cur.fetchone()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if user:
        return User(user[3], user[0], user[4], user[1], user[2], user[5])
    else:
        return None


def car_exists(driver, id_race):
    """ Looks into database if the driver is not added for given race. """

    sql_find_car = """SELECT * from nabidka_spolujizdy WHERE ridic = %s and id_zavod = %s;"""

    conn = get_db()
    
    try:
        cur = conn.cursor()
        cur.execute(sql_find_car, (driver, id_race))
        # execute the SELECT statement
        result = cur.fetchall()
        cur.close()
    finally:
        if conn is not None:
            conn.close()
    return result


def add_carpooling_offer(driver, id_race, departure, departure_date, offer_of_places_in_car, notes):
    """ Adding a new car with a driver into database. """

    sql_najdi_auto = """SELECT * from nabidka_spolujizdy WHERE ridic = %s and id_zavod = %s;"""

    sql_zapis_auto = """INSERT INTO nabidka_spolujizdy(ridic, id_zavod, misto_odjezdu, datum_odjezdu, mist_auto_nabidka, poznamky)
             VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_jizdy; """

    conn = get_db()
    id_ride = None
    
    try:
        cur = conn.cursor()
        cur.execute(sql_najdi_auto, (driver, id_race))
        # execute the SELECT statement
        result = cur.fetchall()
        if result:
            return None
        # execute the INSERT statement
        cur.execute(sql_zapis_auto, (driver, id_race, departure, departure_date, offer_of_places_in_car, notes))
        # get the generated id back
        id_ride = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id_ride


def get_carpool_offers_for_race(id_race):
    """ Returns carpooling offers for the given race. """
    
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
        cur.execute(sql, (id_race,))
        # close communication with the database
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def choose_carpool(id_ride):
    """ Chooses specific id of ride for carpool. """

    sql = """SELECT ns.id_jizdy, ns.id_zavod, jmeno, misto_odjezdu, datum_odjezdu, (mist_auto_nabidka - coalesce(sum_obsazena_mista, 0)) as
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
        cur.execute(sql, (id_ride,))
        # close communication with the database
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def find_count_of_seats(id_ride):
    """ Finds counts of seats for checking the count of asked places during the getting to car. """

    sql = """SELECT ns.id_jizdy, (mist_auto_nabidka - coalesce(sum_obsazena_mista, 0)) as
    volnych_mist FROM
    nabidka_spolujizdy as ns 
    left join 
        (select id_jizdy, sum(chci_mist) as sum_obsazena_mista from 
        spolujezdci as s 
        group by s.id_jizdy) as s
    on ns.id_jizdy = s.id_jizdy
            WHERE ns.id_jizdy=%s;"""

    conn = get_db()
    try:
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql, (id_ride,))
        # close communication with the database
        volnych_mist = cur.fetchone().volnych_mist
        return volnych_mist
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def board_car(id_ride, co_rider, places_wanted):
    """ Inserts co-rider(s) into a database."""

    sql_zjisti = """SELECT * FROM spolujezdci
                   WHERE id_jizdy = %s
                   AND spolujezdec = %s"""

    sql_zapis = """INSERT INTO spolujezdci(id_jizdy, spolujezdec, chci_mist)
                        VALUES(%s, %s, %s);"""


    conn = get_db()

    try:
        cur = conn.cursor()
        cur.execute(sql_zjisti, (id_ride, co_rider))
        # execute the SELECT statement
        vysledek = cur.fetchone()
        if vysledek:
            return False
        cur.execute(sql_zapis, (id_ride, co_rider, places_wanted))
        conn.commit()
        # close communication with the database
        # return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return True


def confirmation_of_carpool(id_ride, co_rider):
    """ Finds a specific ride using id_ride and id_co_rider. """

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
        cur.execute(sql, (id_ride, co_rider))
        # close communication with the database
        return cur.fetchone()
        # print(cur.fetchone())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def change_password(password, id_user):
    """ Changes the user´s password in database. """

    sql = """UPDATE uzivatele
            SET heslo = %s 
            WHERE id_uzivatele = %s;"""
    conn = get_db()
    password = hash_password(password)

    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (password, id_user))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        if conn is not None:
            return True
            conn.close()
