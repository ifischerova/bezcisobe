from flask import Blueprint, render_template
blueprint = Blueprint('heslonew_bp', __name__)
@blueprint.route('/noveheslo')
def show_heslonew():
	return render_template('heslonew.html')