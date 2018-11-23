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
	print('test_hned_za_def')
	result = dict(request.form)
	# result vyse vraci ImmutableDict => nejde do nej nic pridat, proto ho zmenime na normalni dict
	uzivatel = current_user
	if uzivatel.is_authenticated:
		print("Prihlaseny uzivatel je: ", uzivatel.db_id)
	else:
		print("Neni prihlasenej")

	result['ridic'] = uzivatel.db_id
	print('test_pod_ridic')
	print(result)
	id_jizdy = db_funkce.nove_auto(**result)

	if id_jizdy:
		return render_template('autook.html')
		#return redirect(url_for("autook_bp.show_index"))
	else:
		return render_template('autonotok.html')
		#return redirect(url_for("autonotok_bp.show_index"))