from flask import Blueprint, render_template
blueprint = Blueprint('newautoinput_bp', __name__)
@blueprint.route('/noveauto')
def show_newautoinput():
	return render_template('newautoinput.html')