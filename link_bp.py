from flask import Blueprint, render_template
blueprint = Blueprint('link_bp', __name__)
@blueprint.route('/link')
def show_link():
	# pokus o obnovu hesla
	poslano = True

	if poslano:
		return render_template('obnova.html', success=True)
	else:
		return render_template('obnova.html', error="Tento email neexistuje")
