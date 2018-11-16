from flask import Blueprint, render_template
blueprint = Blueprint('autonotok_bp', __name__)
@blueprint.route('/autonotok')
def show_autonotok():
	return render_template('autonotok.html')