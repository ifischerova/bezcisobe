from flask import Blueprint, render_template
blueprint = Blueprint('potvrzeni_registrace_bp', __name__)
@blueprint.route('/registraceOK')
def show_potvrzeni_registrace():
	return render_template('potvrzeni_registrace.html')