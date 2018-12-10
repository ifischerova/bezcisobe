from flask import Blueprint, request, url_for
from flask_login import current_user
import db_funkce 
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
	#tenhle mail by měl odejít ve chvíli, kdy uživatel zadá povinné údaje k přidání auta ke konkrétnímu závodu. 

	#měl by to být email aktuálně přihlášeného uživatele
def email_o_pridani_auta(uzivatel,id_zavod):
	server = smtplib.SMTP('smtp.gmail.com',587)
	#měl by být závod, na který auto přihlásil
	email = uzivatel.id
	zavod = db_funkce.zavod(id_zavod)
	nazev_zavodu = zavod.nazev
	datum = zavod.datum_zavodu.strftime('%d.%m.%Y')
	misto = zavod.misto_zavodu
	zprava = EmailMessage()
	zprava['Subject'] = "Potvrzení o zadání nabídky spolujízdy na závod"
	zprava['From'] = Address('Běžci Sobě', 'bezcisobe', 'gmail.com')
	zprava['To'] = uzivatel.id
	zprava['Message-Id'] = make_msgid()
	text = f"""Ahoj!

	Právě jsi na bezcisobe.cz nabídl/a spolujízdu na následující akci: {datum} {nazev_zavodu} {misto}. 

	Super!

	Přeji prima společnou jízdu a skvělý sportovní zážitek!
	Ivka z Běžci Sobě"""
	zprava.set_content(text)
	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
	mail.ehlo()
	mail.starttls()
	mail.login('bezcisobe@gmail.com','behamespolu')
	mail.sendmail('bezcisobe@gmail.com',email, zprava.as_string())
	mail.close()

def email_o_nastupu_do_auta(uzivatel,id_zavod,id_jizdy):
	server = smtplib.SMTP('smtp.gmail.com',587)
	email = uzivatel.id
	zavod = db_funkce.zavod(id_zavod)
	ridic = db_funkce.posta_ridic(id_jizdy)
	nazev_zavodu = zavod.nazev
	datum = zavod.datum_zavodu.strftime('%d.%m.%Y')
	misto = zavod.misto_zavodu
	sofer = ridic.jmeno
	mobil = ridic.telefon
	email_ridice = ridic.email
	odjezd = ridic.misto_odjezdu
	datum_odj = ridic.datum_odjezdu.strftime('%d.%m.%Y')
	zprava = EmailMessage()
	zprava['Subject'] = "Jedete spolu!"
	zprava['From'] = Address('Běžci Sobě', 'bezcisobe', 'gmail.com')
	zprava['To'] = uzivatel.id
	zprava['Message-Id'] = make_msgid()
	text = f"""Ahoj!

	Právě jsi na bezcisobe.cz potvrdil/a, že chceš jet na {datum} {nazev_zavodu} {misto} s {sofer}. Odjizdite z {odjezd} v terminu {datum_odj}.

	Tady jsou potřebné kontakty  na řidiče:
 	* telefon: {mobil}
 	* mail: {email_ridice}

	Skvělý zážitek přeji!
	Ivka z Běžci Sobě"""
	zprava.set_content(text)
	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
	mail.ehlo()
	mail.starttls()
	mail.login('bezcisobe@gmail.com','behamespolu')
	mail.sendmail('bezcisobe@gmail.com',email, zprava.as_string())
	mail.close()

#mail se odešle ve chvíli kdy někdo nastoupí do nabízeného auta
def email_spolujizda_ridic(uzivatel,id_zavod,id_jizdy):
	server = smtplib.SMTP('smtp.gmail.com',587)
	ridic = db_funkce.email_ridic(id_jizdy)
	zavod = db_funkce.zavod(id_zavod)
	nazev_zavodu = zavod.nazev
	datum = zavod.datum_zavodu.strftime('%d.%m.%Y')
	misto = zavod.misto_zavodu
	jmeno_spolucestujiciho = uzivatel.jmeno #jmeno aktuálně prihlášeného uživatele, který potvrdil nástup do auta
	email_uzivatele = uzivatel.id #uzivatel.id aktuálně prihlášeného uživatele, který potvrdil nástup do auta
	mobil_uzivatele = uzivatel.telefon #telefon aktuálně přihlášeného uživatele, který potvrdil nástup do auta
	zprava = EmailMessage()
	zprava['Subject'] = "Jedete spolu!"
	zprava['From'] = Address('Běžci Sobě', 'bezcisobe', 'gmail.com')
	zprava['To'] = ridic.email
	zprava['Message-Id'] = make_msgid()
	text = f"""Ahoj!

	{jmeno_spolucestujiciho} si Tě právě na bezcisobe.cz vybral/a jako svého řidiče na {datum} {nazev_zavodu} {misto}.

	Tady jsou potřebné kontakty spolucestujícího:
	* telefon: {mobil_uzivatele}
	* mail: {email_uzivatele}

	Doladění detailů už je na vás:)

	Skvelý zážitek přeji!
	Ivka z Běžci Sobě"""
	zprava.set_content(text)
	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
	mail.ehlo()
	mail.starttls()
	mail.login('bezcisobe@gmail.com','behamespolu')
	mail.sendmail('bezcisobe@gmail.com',ridic.email, zprava.as_string())
	mail.close()

def email_reset_hesla(uzivatel, password_reset_url):
	""" Posle mail pro reset hesla."""

	server = smtplib.SMTP('smtp.gmail.com',587)
	email = uzivatel.id
	#password_reset_url = ???
	zprava = EmailMessage()
	zprava['Subject'] = "Žádost o obnovu hesla z Běžci sobě"
	zprava['From'] = Address('Běžci Sobě', 'bezcisobe', 'gmail.com')
	zprava['To'] = uzivatel.id
	zprava['Message-Id'] = make_msgid()
	text = f"""Ahoj!

	Právě jsí na Běžci sobě požádal/a o obnovení zapomenutého hesla.

	Klikni, prosím, na následující link a heslo si resetuj.

	{ password_reset_url }

	Ivka z Běžci Sobě"""
	zprava.set_content(text)
	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
	mail.ehlo()
	mail.starttls()
	mail.login('bezcisobe@gmail.com','behamespolu')
	mail.sendmail('bezcisobe@gmail.com',email, zprava.as_string())
	mail.close()