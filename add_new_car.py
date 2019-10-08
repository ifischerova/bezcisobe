from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
import db_functions
import email_functions


blueprint = Blueprint('addnewcar_bp', __name__)


@blueprint.route('/noveauto', defaults={'id_race': 0})
@blueprint.route('/noveauto/<id_race>', )
def show_add_new_car_form(id_race):
	races = db_functions.get_races()
	variable = request.args
	id_race = variable.get('id_zavod')
	if not id_race:
		id_race = 0
	# print(id_zavod)
	user = current_user

	if user.is_authenticated:
		if int(id_race) > 0:
			result = db_functions.car_exists(user.db_id, id_race)
			if result:
				flash('Na tento závod už auto nabízíš;)', "error")
				return render_template('add_new_car.html', zavody=races, id_vybraneho=int(id_race), values={})
			else: 
				return render_template('add_new_car.html', zavody=races, id_vybraneho=int(id_race), values={})
		else:
			return render_template('add_new_car.html', zavody=races, id_vybraneho=0, values={})
	else:
		flash('Abys mohl/a přidat auto, musíš se nejdřív přihlásit.', "danger")
		return render_template('login.html')


@blueprint.route('/noveauto', methods=['POST'])
def add_new_car():
	result = request.form
	races = db_functions.get_races()
	id_zavod = int(result.get('id_zavod'))

	user = current_user

	id_race = db_functions.add_carpooling_offer(
		user.db_id,
		result.get("id_zavod"),
		result.get("misto_odjezdu"),
		result.get("datum_odjezdu"),
		result.get("mist_auto_nabidka"),
		result.get("poznamky")
	)
	if id_race:
		email_functions.email_new_added_car(user, result.get("id_zavod"))
		flash ('Hotovo! Auto jsme přidali do nabídky spolujízdy na závod a je zpřístupněno zájemcům:) Potvrzení najdeš i ve svém mailu.', 'success')
		return render_template('races.html', zavody=races, id_vybraneho=0)
	else:
		flash('Na tento závod už auto nabízíš.', "danger")
		return render_template('add_new_car.html', zavody=races, values=result)