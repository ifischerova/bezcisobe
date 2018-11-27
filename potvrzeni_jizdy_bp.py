from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import current_user
import db_funkce

blueprint = Blueprint('potvrzeni_jizdy_bp', __name__)
@blueprint.route('/potvrzenijizdy/<zvoleno>')
def show_potvrzenijizdy(zvoleno):
	zvoleno = db_funkce.vyber_spolujizdu(zvoleno)
	uzivatel = current_user
	if uzivatel.is_authenticated:
		return render_template('potvrzeni_jizdy.html', values=zvoleno)
	else:
		return render_template('prihlaseni.html')
	# return render_template('potvrzeni_jizdy.html', values=zvoleno)


@blueprint.route('/potvrzenijizdy/', methods=['POST'])
def chci_nastoupit():
	uzivatel = current_user
	
	if uzivatel.is_authenticated:
		print("Prihlaseny uzivatel je: ", uzivatel.db_id)
	else:
		# TODO: redirect na prihlasovaci stranku
		print("Neni prihlasenej")
	
	id_jizdy = db_funkce.chci_nastoupit(
		int(request.form.get("id_jizdy")),
		uzivatel.db_id,
		int(request.form.get("chci_mist"))
	)
	if id_jizdy:
		return '<h1> Nevyšlo to, v tomhle autě už máš místo rezervované. </h1>'

	souhrn = db_funkce.potvrzeni_spolujizdy(
		int(request.form.get("id_jizdy")),
		uzivatel.db_id
	)
	return render_template('potvrzeni_jizdy_OK.html', success=True, values=souhrn)


'''
@blueprint.route('/potvrzenijizdyOK')
def show_potvrzenijizdyOK():
	potvrzuji = True

	if potvrzuji:
		return render_template('potvrzeni_jizdy_OK.html', success=True)
'''
# Tohle asi muzeme umazat.

	