from flask import Blueprint, current_app, request, render_template, redirect, url_for, flash, abort
# from myapp.models import User
from hashlib import sha512
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from wtforms import Form, TextField, PasswordField, validators, StringField, HiddenField
# https://infinidum.com/2018/08/18/making-a-simple-login-system-with-flask-login/
# pip install flask-wtf flask-login
from db_functions import find_user

from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


class LoginForm(Form):
    email = StringField('email', [validators.DataRequired(), validators.Email(message='Chybný tvar emailové adresy.'), validators.Length(min=4)])
    password = PasswordField('heslo', [validators.DataRequired(), validators.Length(min=6, message = 'Heslo musí být alespoň 6 znaků dlouhé.')])


blueprint = Blueprint('login_bp', __name__)


@blueprint.route('/prihlaseni', methods=['GET', 'POST'])
def login():
    next = get_redirect_target()
    #print(next)
    form = LoginForm(request.form)

    if request.method == 'POST':

        email = request.form["email"]
        password = request.form["heslo"]
        user = find_user(email)
        # uspesne_prihlasen = False
        if user:
            if sha512(password.encode()).hexdigest() != user.password_hash:
                flash('Tohle heslo to nebylo.', "danger")
            elif sha512(password.encode()).hexdigest() == user.password_hash:
                if login_user(user, force=True):
                    flash('Rádi Tě tu zase vidíme.', "success")
                    if next.endswith('prihlaseni') or next.endswith('registrace') or 'noveheslo' in next:
                        return redirect(url_for('races_bp.show_races'))
                    return redirect(next)
        if not user:
            flash("Tenhle email u nás ještě nemáme. Nejprve se, prosím, zaregistruj.", "danger")
            return redirect(url_for('registration_bp.add_new'))

    # TODO: při neúspěšném pokusu o přihlášení zachovat ve formuláři zadaný email??
    return render_template('login.html', form=form)


@blueprint.route('/odhlaseni')
def logout():
    logout_user()
    return redirect(url_for('show_index'))
