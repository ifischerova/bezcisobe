from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
# from wtforms import Form, BooleanField, StringField, PasswordField, validators
import db_funkce


blueprint = Blueprint('registrace_bp', __name__)
@blueprint.route('/registrace')
def show_registrace():
	return render_template('registrace.html', values={})

@blueprint.route('/registrace', methods=['POST'])
def add_new():
	result = request.form
	chyba = None

	uz_registrovany = db_funkce.najdi_uzivatele(result.get("email"))
	if uz_registrovany:
		chyba = 'Zadaný e-mail už existuje v databázi. Můžeš se přihlásit.'

	heslo = result.get("heslo")
	heslo_potvrzeni = result.get("heslo_potvrzeni")
	if not heslo == heslo_potvrzeni:
		chyba = 'Hesla se neshodují.'
		return render_template("registrace.html", values=result, error=chyba)
	
	if not result.get("skrtatko", "") == "ano":
		chyba = 'Prosím, potvrď souhlas se zpracováním osobních údajů.'
		return render_template("registrace.html", values=result, error=chyba)
	
	id_uzivatele = db_funkce.registrace(
		result.get("jmeno"),
		result.get("prijmeni"),
		result.get("ulice"),
		result.get("mesto"),
		result.get("psc"),
		result.get("email"),
		result.get("telefon"),
		heslo,
		heslo_potvrzeni
	)
		# Stačí se jen přihlásit <a class="odkaz" href="{{ url_for('prihlaseni_bp.login') }}">tady.</a>'
		# return redirect(url_for('prihlaseni_bp.login'))

	if id_uzivatele:
		flash('Díky za registraci.')
		return redirect(url_for('prihlaseni_bp.login'))
	else:
		return render_template("registrace.html", values=result, error=chyba)

'''
class RegistrationForm(Form):
	jmeno = StringField('Jméno', [validators.DataRequired()])
	prijmeni = StringField('Příjmení', [validators.DataRequired()])
	ulice = StringField('Ulice,č.p./č.o.', [validators.DataRequired()])
	mesto = StringField('Město', [validators.DataRequired()])
	psc = StringField('PSČ', [validators.Length(min=5, max=5)], [validators.DataRequired()])
	telefon = StringField('Telefon', [validators.Length(min=9, max=15)], [validators.DataRequired()])
	email = StringField('E-mail', [validators.Length(min=6, max=35)], [validators.DataRequired()])
	heslo = PasswordField('Heslo', [validators.DataRequired()])
	heslo_potvrzeni = PasswordField('Potvrzení hesla', [
		validators.DataRequired(),
		validators.EqualTo('heslo_potvrzeni', message='Hesla se musí shodovat.')
	])
	skrtatko = BooleanField('I accept the TOS', [validators.DataRequired()])
'''