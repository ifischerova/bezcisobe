from flask import Blueprint, render_template, request
import db_funkce

blueprint = Blueprint('registrace_bp', __name__)
@blueprint.route('/registrace') # , methods = ['POST'])
def show_registrace():
	#if request.method == 'POST':
      #result = request.form
	return render_template('registrace.html')

@blueprint.route('/registrace', methods=['POST'])
def add_new():
	result = request.form
	db_funkce.registrace(**result)
	#registrace(jmeno, prijmeni, ulice, mesto_obec, PSC, email, telefon, heslo)

