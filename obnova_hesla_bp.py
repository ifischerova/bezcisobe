from flask import Blueprint, render_template
blueprint = Blueprint('obnova_hesla_bp', __name__)
@blueprint.route('/obnovahesla')
def show_obnova():
	return render_template('obnova_hesla.html')

@blueprint.route('/link')
def send_link():
	# pokus o obnovu hesla
	poslano = True

	if poslano:
		return render_template('obnova_hesla.html', success=True)
	else:
		return render_template('obnova_hesla.html', error="Tento email neexistuje.")

@blueprint.route('/noveheslo')
def show_heslonew():
	#zadani noveho hesla, musi byt shodná
	return render_template('noveheslo.html')
	shoda=True

	if poslano:
		return render_template('prihlaseni.html', success=True)
	else:
		return render_template('noveheslo.html', error="Tento email neexistuje.")

