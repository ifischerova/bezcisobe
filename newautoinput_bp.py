from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import current_user
import db_funkce


blueprint = Blueprint('newautoinput_bp', __name__)
@blueprint.route('/noveauto', defaults={'id_zavod':0})
@blueprint.route('/noveauto/<id_zavod>')
def show_newautoinput(id_zavod):
	zavody = db_funkce.zavody()
	promenna = dict(request.args)
	id_zavod = promenna['id_zavod']
	uzivatel = current_user
	if uzivatel.is_authenticated:
		return render_template('newautoinput.html', zavody=zavody, id_vybraneho=int(id_zavod), values={} )
	else:
		return render_template('prihlaseni.html')


@blueprint.route('/noveauto', methods=['POST'])
def add_new_car():
	result = dict(request.form)
	# result vyse vraci ImmutableDict => nejde do nej nic pridat, proto ho zmenime na normalni dict
	uzivatel = current_user
	if uzivatel.is_authenticated:
		print("Prihlaseny uzivatel je: ", uzivatel.db_id)
	else:
		print("Neni prihlasenej")
	result['ridic'] = uzivatel.db_id
	id_jizdy = db_funkce.nove_auto(**result)

	if id_jizdy:
		return render_template('autook.html')
		#return redirect(url_for("autook_bp.show_index"))
	else:
		return render_template('autonotok.html')
		#return redirect(url_for("autonotok_bp.show_index"))