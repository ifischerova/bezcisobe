from flask import Blueprint, render_template, request, redirect,url_for, flash, abort
from flask_login import current_user
import db_funkce
import posta_funkce

blueprint = Blueprint('potvrzeni_jizdy_bp', __name__)
@blueprint.route('/potvrzenijizdy/<zvoleno>')
def show_potvrzenijizdy(zvoleno):
	zvoleno = db_funkce.vyber_spolujizdu(zvoleno)
	uzivatel = current_user
	if uzivatel.is_authenticated:
		return render_template('potvrzeni_jizdy.html', values=zvoleno)
	else:
		flash('Abys mohl nastoupit, musíš se nejdřív přihlásit.')
		return render_template('prihlaseni.html')
	# return render_template('potvrzeni_jizdy.html', values=zvoleno)


@blueprint.route('/potvrzenijizdy/', methods=['POST'])
def chci_nastoupit():
	uzivatel = current_user
	zvoleno = db_funkce.vyber_spolujizdu(request.form.get("id_jizdy"))
	id_zavod=request.form.get("id_zavod")

	if uzivatel.is_authenticated:
		print("Prihlaseny uzivatel je: ", uzivatel.db_id)
	else:
		print("Neni prihlasenej")
	
	volnych_mist = db_funkce.najdi_pocet_mist(int(request.form.get("id_jizdy")))
	if int(request.form.get("chci_mist")) > int(volnych_mist):
		chyba = 'Nevyšlo to, chceš víc míst, než kolik je volných.'
		return render_template('potvrzeni_jizdy.html', values=zvoleno, error=chyba)
	else:
		id_jizdy = db_funkce.chci_nastoupit(
			int(request.form.get("id_jizdy")),
			uzivatel.db_id,
			int(request.form.get("chci_mist"))
			)
		if id_jizdy:
			chyba = 'Nevyšlo to, v tomhle autě už máš místo rezervované.'
			return render_template('potvrzeni_jizdy.html', values=zvoleno, error=chyba)
		else:
			souhrn = db_funkce.potvrzeni_spolujizdy(
			int(request.form.get("id_jizdy")),
			uzivatel.db_id
			)
			posta_funkce.email_o_nastupu_do_auta(uzivatel, id_zavod, id_jizdy)
			return render_template('potvrzeni_jizdy_OK.html', success=True, values=souhrn)


'''
@blueprint.route('/potvrzenijizdyOK')
def show_potvrzenijizdyOK():
	potvrzuji = True

	if potvrzuji:
		return render_template('potvrzeni_jizdy_OK.html', success=True)
'''
# Tohle asi muzeme umazat.

	