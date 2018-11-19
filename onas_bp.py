from flask import Blueprint, render_template
blueprint = Blueprint('onas_bp', __name__)
@blueprint.route('/onas')
def show_onas():
	return render_template('onas.html')