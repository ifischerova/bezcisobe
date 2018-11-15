from flask import Blueprint, render_template, request
import db_funkce

blueprint = Blueprint('pridani_auta_bp', __name__)
@blueprint.route('/registrace') # , methods = ['POST'])
def show_pridani_auta():
	#if request.method == 'POST':
      #result = request.form
	return render_template('/zavody/<id_zavod>')

@blueprint.route('/zavody/<id_zavod>, methods=['POST'])
def add_new_car():
	result = request.form
	db_funkce.nove_auto(**result)


