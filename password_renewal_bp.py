from flask import Blueprint, render_template, request, redirect, flash, abort, url_for, g
from flask_login import current_user, logout_user
import os
import db_functions
from cryptography.fernet import Fernet, InvalidToken
import json
import email_functions

blueprint = Blueprint('password_renewal_bp', __name__)


@blueprint.route('/obnovahesla')
def show_renewal():
	return render_template('password_renewal_email.html')


pw_refresh_token_generator = Fernet(os.environ["PASSWORD_RESET_KEY"].encode("ascii"))


@blueprint.route('/obnovahesla', methods=['POST'])
def renew_password():
	email = request.form.get('email')
	user = db_functions.find_user(email)
	if user:
		flash ('Na zadaný e-mail jsme poslali link pro obnovu hesla.', "success")
		id = user.db_id
		token_data = {"id": id}
		token = pw_refresh_token_generator.encrypt(json.dumps(token_data).encode("ascii")).decode("ascii")
		password_reset_url = url_for('.show_new_password', token=token, _external=True)
		print(password_reset_url)
		email_functions.email_about_reseting_the_password(user, password_reset_url)
		return render_template('password_renewal_email.html')
	else:
		flash('Tento e-mail v naší databázi není.', "danger")
		return render_template('password_renewal_email.html')


@blueprint.route('/noveheslo/<token>')
def show_new_password(token):
	if current_user.is_authenticated:
		logout_user()
		return redirect(url_for('.show_new_password', token=token))
	else:
		try:
			token_data = json.loads(pw_refresh_token_generator.decrypt(token.encode("ascii"), ttl=60 * 60 * 24).decode('UTF-8'))
			#print(token_data)
		except InvalidToken:
			print("Neplatný token.")
			flash("Neplatný link pro obnovení hesla.", "danger")
		return render_template('password_change.html', token=token)


@blueprint.route('/noveheslo', methods=['POST'])
def new_password():
	result = request.form
	token = result.get("token")
	id_user = json.loads(pw_refresh_token_generator.decrypt(token.encode("ascii"), ttl=60 * 60 * 24).decode('UTF-8'))['id']
	password = result.get("password")
	password_confirmation = result.get("password_confirmation")
	if not password == password_confirmation:
		flash('Hesla se neshodují.', "danger")
		return render_template("password_change.html")
	else:
		changed = db_functions.change_password(password, id_user)

	if changed == True:
		flash('Heslo bylo úspěšně změněno. Nyní se můžeš přihlásit.', "success")
		return render_template('login.html')
	else:
		flash('Interní chyba aplikace. Kontaktuj nás, prosím, na bezcisobe@gmail.com')
		return render_template('login.html')
