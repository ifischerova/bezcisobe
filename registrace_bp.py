from flask import Blueprint, render_template
blueprint = Blueprint('registrace_bp', __name__)
@blueprint.route('/registrace')
def show_registrace():
	return render_template('registrace.html')