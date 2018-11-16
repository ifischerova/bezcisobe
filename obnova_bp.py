from flask import Blueprint, render_template
blueprint = Blueprint('obnova_bp', __name__)
@blueprint.route('/obnova')
def show_obnova():
	return render_template('obnova.html')

@blueprint.route('/link')
def send_link():
	# pokus o obnovu hesla
	poslano = True

	if poslano:
		return render_template('obnova.html', success=True)
	else:
		return render_template('obnova.html', error="Tento email neexistuje")
