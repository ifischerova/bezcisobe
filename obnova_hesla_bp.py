from flask import Blueprint, render_template, request, flash, abort, url_for, g
import os
import db_funkce
from cryptography.fernet import Fernet, InvalidToken
import json
import posta_funkce

blueprint = Blueprint('obnova_hesla_bp', __name__)
@blueprint.route('/obnovahesla')
def show_obnova():
	return render_template('obnova_hesla.html')


f = Fernet(os.environ["PASSWORD_RESET_KEY"].encode("ascii"))
@blueprint.route('/obnovahesla', methods=['POST'])
def find_user():
	email = request.form.get('email')
	uzivatel = db_funkce.najdi_uzivatele(email)
	if uzivatel:
		flash ('Na zadaný e-mail jsme poslali link pro obnovu hesla.', "success")
		id = uzivatel.db_id
		token_data = {"id": id}
		f = Fernet(os.environ["PASSWORD_RESET_KEY"].encode("ascii"))
		token = f.encrypt(json.dumps(token_data).encode("ascii")).decode("ascii")
	else:
		flash ('Tento e-mail v naší databázi není.', "danger")

@blueprint.route('/noveheslo/<token>')
def show_heslonew():
	token = request.args.get('token')
	try:
		token_data = json.loads(f.decrypt(token.encode("ascii"), ttl=60*60*24))
	except InvalidToken:
		print("Neplatný token.")
		flash ("Neplatný link.", "danger")
	return render_template('noveheslo.html')


@blueprint.route('/noveheslo', methods=['POST'])
def heslo_new(id_uzivatele, heslo):
	result = request.form
	chyba = None
	id_uzivatele = request.args.get('token_data')

	heslo = result.get("heslo")
	heslo_potvrzeni = result.get("heslo_potvrzeni")
	if not heslo == heslo_potvrzeni:
		flash ('Hesla se neshodují.', "danger")
		return render_template("noveheslo.html", error=chyba)
	else:
		zmeneno = db_funkce.zmena_hesla(result.get("heslo"), id_uzivatele)

	if zmeneno == True:
		flash ('Heslo bylo úspěšně změněno. Nyní se můžeš přihlásit.', "success")
		
'''
	if poslano:
		return render_template('obnova_hesla.html', success=True)
	else:
		return render_template('obnova_hesla.html', error="Tento email neexistuje.")

@blueprint.route('/noveheslo')
def show_heslonew():
	#zadani noveho hesla, musi byt shodná
	return render_template('noveheslo.html')
	shoda=True

	if poslano:
		return render_template('prihlaseni.html', success=True)
	else:
		return render_template('noveheslo.html', error="Tento email neexistuje.")

'''