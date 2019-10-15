from flask import Blueprint, request, url_for
from flask_login import current_user
import db_functions
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid


def send_email(recipient_address, email_subject, text):
	"""  This email should be sent when user sets required data for adding a new car to specific race.
		Should be an email of signed in user. """
	message = EmailMessage()
	message['Subject'] = email_subject
	message['From'] = Address('Běžci Sobě', 'bezcisobe', 'gmail.com')
	message['To'] = recipient_address
	message['Message-Id'] = make_msgid()
	message.set_content(text)

	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
	mail.ehlo()
	mail.starttls()
	mail.login('bezcisobe@gmail.com','behamespolu')
	mail.sendmail('bezcisobe@gmail.com',recipient_address, message.as_string())
	mail.close()


def email_new_added_car(user, id_race):
	""" Should be a race for which is the car signed in. """
	email = user.id
	race = db_functions.get_race(id_race)
	name_of_race = race.nazev
	date = race.datum_zavodu.strftime('%d.%m.%Y')
	place = race.misto_zavodu
	subject = "Potvrzení o zadání nabídky spolujízdy na závod"
	text = """Ahoj!

	Právě jsi na bezcisobe.cz nabídl/a spolujízdu na následující akci: {date} {name_of_race} {place}. 

	Super!

	Přeji prima společnou jízdu a skvělý sportovní zážitek!
	Ivka z Běžci Sobě""".format(date=date, name_of_race=name_of_race,place=place)

	send_email(email, subject, text)

def email_board_on_car(user, id_race, id_ride):
	""" Email is sent when someone boards on the car. """
	email = user.id
	race = db_functions.get_race(id_race)
	driver = db_functions.get_ride_confirmation_details(id_ride)
	name_of_race = race.nazev
	date = race.datum_zavodu.strftime('%d.%m.%Y')
	place_of_race = race.misto_zavodu
	chauffeur = driver.jmeno
	mobile_phone = driver.telefon
	email_driver = driver.email
	departure = driver.misto_odjezdu
	date_of_departure = driver.datum_odjezdu.strftime('%d.%m.%Y')
	subject = "Jedete spolu!"
	
	text = """Ahoj!

	Právě jsi na bezcisobe.cz potvrdil/a, že chceš jet na {date} {name_of_race} {place_of_race} s {chauffeur}. Odjizdite z {departure} v terminu {date_of_departure}.

	Tady jsou potřebné kontakty  na řidiče:
 	* telefon: {mobile_phone}
 	* mail: {email_driver}

	Skvělý zážitek přeji!
	Ivka z Běžci Sobě""".format(date=date, name_of_race=name_of_race, place_of_race=place_of_race, chauffeur=chauffeur, departure=departure, date_of_departure=date_of_departure, mobile_phone=mobile_phone, email_driver=email_driver)

	send_email(email, subject, text)


def email_to_carpool_driver(user, id_race, id_ride):
	""" Email is sent when someone boards on the car. """
	driver = db_functions.get_ride_driver(id_ride)
	race = db_functions.get_race(id_race)
	name_of_race = race.nazev
	date = race.datum_zavodu.strftime('%d.%m.%Y')
	place = race.misto_zavodu
	co_driver_name = user.jmeno #signed user´s name who confirmed boarding on car
	email_user = user.id #signed user´s uzivatel.id who confirmed boarding on car
	mobilephone_user = user.telefon #signed user´s phone who confirmed boarding on car
	subject = "Jedete spolu!"

	text = """Ahoj!

	{co_driver_name} si Tě právě na bezcisobe.cz vybral/a jako svého řidiče na {date} {name_of_race} {place}.

	Tady jsou potřebné kontakty spolucestujícího:
	* telefon: {mobilephone_user}
	* mail: {email_user}

	Doladění detailů už je na vás:)

	Skvělý zážitek přeji!
	Ivka z Běžci Sobě""".format(co_driver_name=co_driver_name, date=date, name_of_race=name_of_race, place=place, mobilephone_user=mobilephone_user, email_user=email_user)

	send_email(driver.email, subject, text)

def email_about_reseting_the_password(user, password_reset_url):
	""" Sents email with link for reseting the password."""

	email = user.id
	#password_reset_url = ???
	subject = "Žádost o obnovu hesla na Běžci Sobě"
	text = """Ahoj!

	Právě jsi na Běžci sobě požádal/a o obnovení zapomenutého hesla.

	Klikni, prosím, na následující link a heslo si resetuj.

	{password_reset_url}

	Petra z Běžci Sobě""".format(password_reset_url=password_reset_url)

	send_email(email, subject, text)
