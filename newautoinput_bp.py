from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import current_user
import db_funkce
import posta_funkce


blueprint = Blueprint('newautoinput_bp', __name__)
@blueprint.route('/noveauto', defaults={'id_zavod':0})
@blueprint.route('/noveauto/<id_zavod>')
def show_newautoinput(id_zavod):
	zavody = db_funkce.zavody()
	promenna = request.args
	id_zavod = promenna.get('id_zavod')
	uzivatel = current_user
	if uzivatel.is_authenticated:
		vysledek = db_funkce.uz_existuje_auto(uzivatel.db_id, id_zavod)
		if vysledek:
			return render_template('autonotok.html')
		else:
			return render_template('newautoinput.html', zavody=zavody, id_vybraneho=int(id_zavod), values={} )
	else:
		return render_template('prihlaseni.html')


@blueprint.route('/noveauto', methods=['POST'])
def add_new_car():
	result = request.form
	
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
		return render_template('autook.html')
		#return redirect(url_for("autook_bp.show_index"))
	else:
		return render_template('autonotok.html')
		#return redirect(url_for("autonotok_bp.show_index"))