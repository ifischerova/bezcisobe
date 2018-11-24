from flask import Blueprint, current_app, request, render_template, redirect, url_for
# from myapp.models import User
from hashlib import sha512
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from wtforms import Form, TextField, PasswordField, validators
# https://infinidum.com/2018/08/18/making-a-simple-login-system-with-flask-login/
# pip install flask-wtf flask-login
from db_funkce import najdi_uzivatele


class LoginForm(Form):
    email = TextField('email', [validators.Required(), validators.Length(min=4, max=25)])
    password = PasswordField('heslo', [validators.Required(), validators.Length(min=6, max=200)])


blueprint = Blueprint('prihlaseni_bp', __name__)

@blueprint.route('/prihlaseni', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    chyba = None
    if request.method == 'POST':
        # TODO: validace poli formulare??

        email = request.form["email"]
        heslo = request.form["heslo"]
        uzivatel = najdi_uzivatele(email)
        uspesne_prihlasen = False
        if uzivatel:
            if sha512(heslo.encode()).hexdigest() == uzivatel.password_hash:
                if login_user(uzivatel, force=True):
                    uspesne_prihlasen = True
                    return redirect(url_for('about_bp.show_index'))
        
        if not uspesne_prihlasen:
            chyba = "Neplatné přihlašovací údaje"

    # TODO: zobrazit upozorneni o spatne zadanem jmenu/heslu
    # TODO: presmerovani po uspesnem prihlaseni - kam?
    # TODO: při neúspěšném pokusu o přihlášení zachovat ve formuláři zadaný email
    return render_template('prihlaseni.html', form=form, chyba=chyba)

@blueprint.route('/odhlaseni')
def logout():
    logout_user()
    return redirect(url_for('about_bp.show_index'))
