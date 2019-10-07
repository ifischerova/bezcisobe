from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
import db_functions
import email_functions

blueprint = Blueprint('ride_confirmation_bp', __name__)


@blueprint.route('/potvrzenijizdy/<chosen>')
def show_ride_confirmation(chosen):
	chosen = db_functions.choose_carpool(chosen)
	user = current_user
	if user.is_authenticated:
		return render_template('potvrzeni_jizdy.html', values=chosen)
	else:
		flash('Abys mohl nastoupit, musíš se nejdřív přihlásit.', "danger")
        return render_template('login.html')


@blueprint.route('/potvrzenijizdy/', methods=['POST'])
def confirm_ride():
	user = current_user
	chosen = db_functions.choose_carpool(request.form.get("id_jizdy"))
	id_race = request.form.get("id_zavod")
	id_ride = request.form.get("id_jizdy")

    free_carplaces = db_functions.find_count_of_seats(int(request.form.get("id_jizdy")))
	if int(request.form.get("chci_mist")) > int(free_carplaces):
		flash('Bohužel chceš víc míst, než kolik jich je volných.', "danger")
		return render_template('potvrzeni_jizdy.html', values=chosen)
	else:
        possible_to_board_on = db_functions.board_car(
			int(request.form.get("id_jizdy")),
			user.db_id,
			int(request.form.get("chci_mist"))
			)
		if possible_to_board_on:
			summary = db_functions.confirmation_of_carpool(
			int(request.form.get("id_jizdy")),
			user.db_id
			)
			email_functions.email_to_carpool_driver(user, id_race, id_ride)
			email_functions.email_board_on_car(user, id_race, id_ride)
			flash("Hotovo! V mailu najdeš kontakt na řidiče. On už zase ví o Tobě. "
				  "Doladit detaily už je na vás. My přejeme pohodovou cestu a skvělý sportovní zážitek!", "success")
			return render_template('potvrzeni_jizdy_OK.html', success=True, values=summary)
		else:
			flash('V tomto autě už máš místo rezervované.', "danger")
			return render_template('potvrzeni_jizdy.html', values=chosen)