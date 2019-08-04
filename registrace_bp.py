from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, validators
from flask_wtf import FlaskForm
from flask_login import current_user
import db_funkce


class RegistrationForm(FlaskForm):
    username = StringField(
        'Jméno*:', [validators.Required(message='Bez jména to nepůjde.')])
    surname = StringField(
        'Příjmení*:', [validators.Required(message='Bez příjmení to nepůjde.')])
    street = StringField('Ulice,č.p./č.o.:')
    city = StringField(
        'Město/Obec*:', [validators.Required(message='Vyplň město, kde bydlíš.')])
    postcode = IntegerField('PSČ*:', [validators.Required(message='Bez PSČ to nepůjde.'),
                                      validators.Length(min=5, max=5, message='PSČ zadej bez mezer.')])
    email = StringField('E-mail*:', [validators.Required(message='Bez mailu to nepůjde.', ),
                                     validators.Email(message='Chybný tvar emailové adresy.'), validators.Length(min=4, max=250)])
    phone = IntegerField('Telefon*:', [validators.Required(message='Bez telefonního čísla to nepůjde.'), '''validators.Length(
        min=11, max=11, message='Telefonní číslo zadej bez předvolby a ve tvaru xxx xxx xxx.')'''])
    password = PasswordField('Heslo*:', [validators.Required(message='Bez hesla to nepůjde.'), validators.EqualTo(
        'confirm_password', message='Hesla se musejí shodovat.'), validators.Length(min=8, message='Heslo musí být alespoň 6 znaků dlouhé.')])
    confirm_password = PasswordField(
        'Potvrzení hesla*:', [validators.Required(message='Zadané heslo je třeba potvrdit.')])
    gdpr = BooleanField('Souhlasím ze zpracováním osobních údajů.*', [validators.Required(
        message='Bez udělení Tvého souhlasu Tě nemůžeme zaregistrovat.')])


blueprint = Blueprint('registrace_bp', __name__)


@blueprint.route('/registrace')
def show_registrace():
    uzivatel = current_user
    form = RegistrationForm()

    if uzivatel.is_authenticated:
        flash('Už jsi přihlášen.', "danger")
        return redirect(url_for('zavody_bp.show_zavody'))
    return render_template('registrace.html', values={}, form=form)


@blueprint.route('/registrace', methods=['POST', 'GET'])
def add_new():
    result = request.form
    chyba = None
    form = RegistrationForm()

    if form.validate_on_submit():
        uz_registrovany = db_funkce.najdi_uzivatele(result.get("email"))
        if uz_registrovany:
            flash('Už jsi u nás byl/a, tak se prosím přihlaš.', "danger")
            return redirect(url_for('prihlaseni_bp.login'))

        heslo = result.get("password")
        heslo_potvrzeni = result.get("confirm_password")
        if not heslo == heslo_potvrzeni:
            flash('Hesla se neshodují.', "danger")
            return render_template("registrace.html", values=result, error=chyba, form=form)

        id_uzivatele = db_funkce.registrace(
            result.get("username"),
            result.get("surname"),
            result.get("street"),
            result.get("city"),
            result.get("postcode"),
            result.get("email"),
            result.get("phone"),
            heslo,
            heslo_potvrzeni
        )

        if id_uzivatele:
            flash('Vítáme Tě! Teď se prosím přihlaš.', "success")
            return render_template('prihlaseni.html')
        else:
            flash(
                'Mrzí nás to, ale registrace se nepovedla. Dej nám pár minut a zkus to znovu.', "danger")
            return render_template("registrace.html", values=result, error=chyba, form=form)
    else:
        return render_template("registrace.html", values=result, form=form)
