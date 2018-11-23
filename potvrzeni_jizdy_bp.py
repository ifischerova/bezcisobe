from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import current_user
import db_funkce

blueprint = Blueprint('potvrzeni_jizdy_bp', __name__)
@blueprint.route('/potvrzenijizdy/<zvoleno>')
def show_potvrzenijizdy(zvoleno):
	zvoleno = db_funkce.vyber_spolujizdu(zvoleno)
	return render_template('potvrzeni_jizdy.html', values=zvoleno)


@blueprint.route('/potvrzenijizdy', methods=['POST'])
def chci_nastoupit():
	uzivatel = current_user
	if uzivatel.is_authenticated:
		print("Prihlaseny uzivatel je: ", uzivatel.db_id)
	else:
		print("Neni prihlasenej")

	parametry = dict()
	# Vytvorim novy slovnik, ktery plnim.
	parametry['chci_mist'] = int(request.form['chci_mist'])
	parametry['id_jizdy'] = int(request.form['id_jizdy'])
	# Prevadi hodnoty ze stringu na cisla, coz vyzaduje pro zapis dtb.
	parametry['spolujezdec'] = uzivatel.db_id
	db_funkce.chci_nastoupit(**parametry)
	print(parametry)
	return render_template('potvrzeni_jizdy_OK.html', success=True)


@blueprint.route('/potvrzenijizdyOK')
def show_potvrzenijizdyOK():
	potvrzuji = True

	if potvrzuji:
		return render_template('potvrzeni_jizdy_OK.html', success=True)

	