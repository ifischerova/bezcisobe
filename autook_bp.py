from flask import Blueprint, render_template
blueprint = Blueprint('autook_bp', __name__)
@blueprint.route('/autook')
def show_autook():
	return render_template('autook.html')