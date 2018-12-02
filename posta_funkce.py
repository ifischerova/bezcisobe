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
	zprava.set_content("Ahoj, právě jsi na bezcisobe.cz nabídl/a spolujízdu na následující akci:" + ' ' + datum + ' ' + nazev_zavodu + ' ' + misto + ". Díky, příjemné spolucestující a super sportovní zážitek přeji! Ivka z Běžci sobě", "plain", "utf-8")
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
	zprava.set_content("Ahoj, právě jsi na bezcisobe.cz potvrdil/a, že chceš jet na:" + ' ' + datum + ' ' + nazev_zavodu + ' ' + misto + "s" + sofer + ' ' + odjezd + ' ' + datum_odj + ". Tady přikládáme potřebné kontakty:" + ' ' + mobil + ' ' + email_ridice + ' ' + ". Skvělý sportovní zážitek přeji! Ivka z Běžci Sobě", "plain", "utf-8")
	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
	mail.ehlo()
	mail.starttls()
	mail.login('bezcisobe@gmail.com','behamespolu')
	mail.sendmail('bezcisobe@gmail.com',email, zprava.as_string())
	mail.close()