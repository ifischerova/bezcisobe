#From Flask module import Flask and g for using them in this program.
import os
from flask import Flask, g, render_template
from flask_login import LoginManager

import races_bp

import about_us_bp

import registration_bp

import login_bp

import password_renewal_bp

import addnewcar_bp

import ride_confirmation_bp

from db_functions import find_user


bezciSobe = Flask(__name__)
# Attempt to set a server_name from env because of full url for enable to change password (actually will maybe return http://0.0.0.0/
#bezciSobe.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')
bezciSobe.secret_key = b"\xc1'\xa6T<\x85\x9b\x9d\xdc\x96\x83\x9cx\xad\xf0v"
login_manager = LoginManager()
login_manager.init_app(bezciSobe)


@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return find_user(user_id)


bezciSobe.register_blueprint(races_bp.blueprint)
bezciSobe.register_blueprint(about_us_bp.blueprint)
bezciSobe.register_blueprint(registration_bp.blueprint)
bezciSobe.register_blueprint(login_bp.blueprint)
bezciSobe.register_blueprint(password_renewal_bp.blueprint)
bezciSobe.register_blueprint(addnewcar_bp.blueprint)
bezciSobe.register_blueprint(ride_confirmation_bp.blueprint)


#Registers the function db.close() to our application. This function should start to run when our application terminates.


@bezciSobe.route('/')
def show_index():
    return render_template('index.html')


@bezciSobe.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        # Safely close the connection to our database.
        g.db.close()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bezciSobe.run(host='0.0.0.0', port=port, debug=True)
   
