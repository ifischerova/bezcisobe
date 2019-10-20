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
    # database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require', cursor_factory=psycopg2.extras.NamedTupleCursor)
        g.db = con
    return g.db


def get_races():
    """ Returns list of get_races in decreasing order by date. """

    sql = """SELECT id_race, date_race, place_race, latitude, longitude, name_race FROM races ORDER BY date_race DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data


def get_race(id_race):
    """ Returns date of race, place of race and name of race in the email. """

    sql = """SELECT date_race, place_race, name_race FROM races WHERE id_race = %s"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, (id_race, ))
    data = cur.fetchone()
    return data


def get_ride_confirmation_details(id_ride):
    """ Returns name of driver, place of departure, date of departure, email and phone into an email with confirmation of the boarding to the car. """

    sql = """SELECT u.id_user, u.name, u.phone, u.email, co.driver, co.departure_place, co.departure_date, co.id_ride FROM users AS u LEFT JOIN 
             (SELECT co.driver, co.departure_place, co.departure_date, co.id_ride FROM carpool_offer AS co) AS co ON u.id_user = co.driver WHERE id_ride = %s"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql, (int(id_ride),))
    data = cur.fetchone()
    return data


def get_ride_driver(id_ride):
    """ Returns email of driver for a email field, that is sended to the driver at moment of confirmation of the boarding to his/her offered car."""

    sql = """SELECT u.id_user, u.email, co.driver FROM users AS u LEFT JOIN (SELECT co.driver, co.id_ride FROM carpool_offer AS co) AS co ON co.driver = u.id_user WHERE id_ride = %s"""
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

    sql = """INSERT INTO users (name, surname, street, city, postcode, email, phone, password, latitude, longitude) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_user;"""
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

    sql = """SELECT id_user, name, surname, email, password, phone FROM users WHERE lower(email) = %s;"""
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

    sql_find_car = """SELECT id_ride, driver, id_race, departure_place, departure_date, carseats_offer, notes FROM carpool_offer WHERE driver = %s AND id_race = %s;"""

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

    sql_find_car = """SELECT id_ride, driver, id_race, departure_place, departure_date, carseats_offer, notes FROM carpool_offer WHERE driver = %s AND id_race = %s;"""

    sql_insert_car = """INSERT INTO carpool_offer(driver, id_race, departure_place, departure_date, carseats_offer, notes) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_ride; """

    conn = get_db()
    id_ride = None
    
    try:
        cur = conn.cursor()
        cur.execute(sql_find_car, (driver, id_race))
        # execute the SELECT statement
        result = cur.fetchall()
        if result:
            return None
        # execute the INSERT statement
        cur.execute(sql_insert_car, (driver, id_race, departure, departure_date, offer_of_places_in_car, notes))
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
    
    sql = """ SELECT co.id_ride, co.name, co.departure_place, co.departure_date, (carseats_offer - coalesce(sum_occupied_seats, 0)) AS co.free_seats, co.notes FROM
              carpool_offer AS co LEFT JOIN (SELECT c.id_ride, sum(c.seats_wanted) AS sum_occupied_seats FROM co_riders AS c GROUP BY c.id_ride) AS c ON 
              co.id_ride = c.id_ride LEFT JOIN (SELECT NAME, u.id_user FROM users AS u) AS u ON co.driver = u.id_user WHERE (carseats_offer > sum_occupied_seats 
              OR c.id_ride IS NULL) AND id_race = %s ORDER BY departure_place; """
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

    sql = """SELECT co.id_ride, co.id_race, co.name, co.departure_place, co.departure_date, (co.carseats_offer - coalesce(sum_occupied_seats, 0)) AS co.free_seats, co.notes FROM
             carpool_offer AS co LEFT JOIN (SELECT c.id_ride, sum(c.seats_wanted) AS sum_occupied_seats FROM co_drivers AS c GROUP BY c.id_ride) AS c ON co.id_ride 
             = c.id_ride LEFT JOIN (SELECT NAME, u.id_user FROM u.users AS u) AS u ON co.driver = u.id_user WHERE co.id_ride = %s;"""

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

    sql = """SELECT co.id_ride, (co.carseats_offer - coalesce(sum_occupied_seats, 0)) AS co.free_seats FROM carpool_offer AS co LEFT JOIN (SELECT c.id_ride, sum(c.seats_wanted)
             AS sum_occupied_seats FROM co_drivers AS c GROUP BY c.id_ride) AS c ON co.id_ride = c.id_ride WHERE co.id_ride = %s;"""

    conn = get_db()
    try:
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql, (id_ride,))
        # close communication with the database
        free_seats = cur.fetchone().free_seats
        return free_seats
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def board_car(id_ride, co_rider, places_wanted):
    """ Inserts co-rider(s) into a database."""

    sql_find = """SELECT id_ride, co_rider, seats_wanted FROM co_riders WHERE id_ride = %s AND co_rider = %s"""

    sql_insert = """INSERT INTO co_riders(id_ride, co_rider, seats_wanted) VALUES(%s, %s, %s);"""

    conn = get_db()

    try:
        cur = conn.cursor()
        cur.execute(sql_find, (id_ride, co_rider))
        # execute the SELECT statement
        result = cur.fetchone()
        if result:
            return False
        cur.execute(sql_insert, (id_ride, co_rider, places_wanted))
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

    sql = """SELECT co.id_ride, co.name, co.departure_place, co.departure_date, c.seats_wanted, c.co_rider, c.notes FROM carpool_offer AS co LEFT JOIN (SELECT c.id_ride, c.co_rider, c.seats_wanted FROM 
             co_riders AS c) AS c ON co.id_ride = c.id_ride LEFT JOIN (SELECT NAME, u.id_user FROM users AS u) AS u ON co.driver = u.id_user WHERE co.id_ride = %s AND c.co_rider = %s;"""

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

    sql = """UPDATE users SET password = %s WHERE id_user = %s;"""
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
