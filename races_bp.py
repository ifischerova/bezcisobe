# Import a lot of functions that we need from Flask
from flask import Blueprint, render_template, request, flash, abort
import db_functions
import races_functions

blueprint = Blueprint('races_bp', __name__)


# Registers the function show_races() as a function, which should be called by Flask if user opens page
# "/zavody" in the browser

@blueprint.route('/zavody/')
def show_races():
    # Calls function render_template(), which takes template about.html and
    # generates HTML that is returned as a result of these function to the Flask.
    # Flask sends this result to the user´s browser
    race_date = request.args.get('date_race', default='', type=str)
    id_race = request.args.get('id_race', default=0, type=int)

    carpool_offer = []
    if race_date:
        races = races_functions.races_for_date(race_date)
        if races == []:
            flash('Pro tento den není v databázi žádný závod.', "warning")
            races = db_functions.get_races()
    else:
        races = db_functions.get_races()
    if id_race:
        carpool_offer = db_functions.get_carpool_offers_for_race(id_race)

    return render_template('races.html', races=races, date_race=race_date, id_chosen=id_race,
                           carpool_offer=carpool_offer)
