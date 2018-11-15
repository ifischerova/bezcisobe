from flask import Blueprint, render_template
blueprint = Blueprint('prihlaseni_bp', __name__)
@blueprint.route('/prihlaseni')
def show_prihlaseni():
	return render_template('prihlaseni.html')