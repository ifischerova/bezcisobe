# Z modulu flask naimportuje "Flask" a "g" tak, abychom je mohli
# používat v tomto programu
import os
from flask import Flask, g
from flask_login import LoginManager
# Stejně tak pro about_bp modul

import about_bp

import zavody_bp

import onas_bp

import registrace_bp

import prihlaseni_bp

import obnova_hesla_bp

import newautoinput_bp

import potvrzeni_jizdy_bp

from db_funkce import najdi_uzivatele


bezciSobe = Flask(__name__)
# pokus o nastaveni server_name z env kvuli plnemu url na obnovu hesla (aktualne bude mozna vracet http://0.0.0.0/
#bezciSobe.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')
bezciSobe.secret_key = b"\xc1'\xa6T<\x85\x9b\x9d\xdc\x96\x83\x9cx\xad\xf0v"
login_manager = LoginManager()
login_manager.init_app(bezciSobe)

@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return najdi_uzivatele(user_id)

# Stejně tak zaregistrujeme about_bp blueprint
bezciSobe.register_blueprint(about_bp.blueprint)
bezciSobe.register_blueprint(zavody_bp.blueprint)
bezciSobe.register_blueprint(onas_bp.blueprint)
bezciSobe.register_blueprint(registrace_bp.blueprint)
bezciSobe.register_blueprint(prihlaseni_bp.blueprint)
bezciSobe.register_blueprint(obnova_hesla_bp.blueprint)
bezciSobe.register_blueprint(newautoinput_bp.blueprint)
bezciSobe.register_blueprint(potvrzeni_jizdy_bp.blueprint)
#bezciSobe.register_blueprint(potvrzeni_jizdy_bp.blueprint)
# Zaregistruje funkci close_db() do naší aplikace jako funkci, která se má spustit,
# když se ukončuje naše aplikace

@bezciSobe.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        # Bezpečně ukončí spojení s naší databází
        g.db.close()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bezciSobe.run(host='0.0.0.0', port=port, debug=True)
   
