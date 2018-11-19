from flask import Blueprint, current_app, request, render_template, redirect, url_for
# from myapp.models import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from wtforms import Form, TextField, PasswordField, validators
# https://infinidum.com/2018/08/18/making-a-simple-login-system-with-flask-login/
# pip install flask-wtf flask-login

class LoginForm(Form):
    username = TextField('Username', [validators.Required(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=6, max=200)])

class User(UserMixin):
    def __init__(self,id):
        self.id = id

blueprint = Blueprint('prihlaseni_bp', __name__)
@blueprint.route('/prihlaseni')
def show_prihlaseni():
    return render_template('prihlaseni.html')


@blueprint.route('/prihlaseni', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=username.lower()).first()
        if user:
            if login_user(user):
                current_app.logger.debug('Logged in user %s', user.username)
                return redirect(url_for('secret'))
        error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)
