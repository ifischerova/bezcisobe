from flask import Blueprint, render_template, request, redirect,url_for, flash, abort
from flask_login import current_user
import db_funkce
import posta_funkce


blueprint = Blueprint('newautoinput_bp', __name__)
@blueprint.route('/noveauto', defaults={'id_zavod':0})
@blueprint.route('/noveauto/<id_zavod>', )
def show_newautoinput(id_zavod):
	zavody = db_funkce.zavody()
	promenna = request.args
	id_zavod = promenna.get('id_zavod')
	if not id_zavod:
		id_zavod = 0
	# print(id_zavod)
	uzivatel = current_user

	if uzivatel.is_authenticated:
		if int(id_zavod) > 0:
			vysledek = db_funkce.uz_existuje_auto(uzivatel.db_id, id_zavod)
			if vysledek:
				flash ('Na tento závod už auto nabízíš;)', "error")
				return render_template('newautoinput.html', zavody=zavody, id_vybraneho=int(id_zavod), values={}, error=chyba)
			else: 
				return render_template('newautoinput.html', zavody=zavody, id_vybraneho=int(id_zavod), values={})
		else:
			return render_template('newautoinput.html', zavody=zavody, id_vybraneho=0, values={})
	else:
		flash ('Abys mohl/a přidat auto, musíš se nejdřív přihlásit.', "danger")
		return render_template('prihlaseni.html')


@blueprint.route('/noveauto', methods=['POST'])
def add_new_car():
	result = request.form
	zavody = db_funkce.zavody()
	id_zavod = int(result.get('id_zavod'))

	uzivatel = current_user
	if uzivatel.is_authenticated:
		print("Prihlaseny uzivatel je: ", uzivatel.db_id)
	else:
		print("Neni prihlasenej")
	
	id_jizdy = db_funkce.nove_auto(
		uzivatel.db_id,
		result.get("id_zavod"),
		result.get("misto_odjezdu"),
		result.get("datum_odjezdu"),
		result.get("mist_auto_nabidka"),
		result.get("poznamky")
	)
	if id_jizdy:
		posta_funkce.email_o_pridani_auta(uzivatel, result.get("id_zavod"))
		#return render_template('autook.html')
		flash ('Hotovo! Auto jsme přidali do nabídky spolujízdy na závod a je zpřístupněno zájemcům:) Potvrzení najdeš i ve svém mailu.', 'success')
		return render_template ('zavody.html', zavody=zavody, id_vybraneho=0)
	else:
		flash ('Na tento závod už auto nabízíš.', "danger")
		return render_template('newautoinput.html', zavody=zavody, values=result)