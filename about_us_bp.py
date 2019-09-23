from flask import Blueprint, render_template
blueprint = Blueprint('about_us_bp', __name__)
@blueprint.route('/onas')
def show_about_us():
	return render_template('onas.html')