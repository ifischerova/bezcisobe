from flask import Blueprint, render_template
blueprint = Blueprint('potvrzeni_jizdy_bp', __name__)
@blueprint.route('/potvrzenijizdy')
def show_potvrzenijizdy():
	return render_template('potvrzeni_jizdy.html')

@blueprint.route('/potvrzenijizdyOK')
def show_potvrzenijizdyOK():
	potvrzuji = True

	if potvrzuji:
		return render_template('potvrzeni_jizdy_OK.html', success=True)

	