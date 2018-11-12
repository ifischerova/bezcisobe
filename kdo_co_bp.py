from flask import Blueprint, render_template
blueprint = Blueprint('kdo_co_bp', __name__)
@blueprint.route('/kdoco')
def show_kdo_co():
	return render_template('kdo_co.html')