from flask import Blueprint, render_template, request, redirect,url_for
from flask_login import current_user
import db_funkce


blueprint = Blueprint('newautoinput_bp', __name__)
@blueprint.route('/noveauto')
def show_newautoinput():
	zavody = db_funkce.zavody()
	return render_template('newautoinput.html', zavody=zavody, values={} )


@blueprint.route('/noveauto', methods=['POST'])
def add_new_car():
	result = dict(request.form)
	# result vyse vraci ImmutableDict => nejde do nej nic pridat, nize si zmenime na normalni dict
	uzivatel = current_user
	if uzivatel.is_authenticated:
		print("Prihlaseny uzivatel je: ", uzivatel.db_id)
	else:
		print("Neni prihlasenej")

	# Tohle musime nahradit id prihlaseneho uzivatele, az zprovoznime prihlaseni!!
	result['ridic'] = 1
	id_jizdy = db_funkce.nove_auto(**result)

	if id_jizdy:
		#print('probehlo')
		return render_template('autook.html')
		#return redirect(url_for("autook_bp.show_index"))
	else:
		return render_template('autonotok.html')
		#print('neprobehlo')
		#return redirect(url_for("autonotok_bp.show_index"))