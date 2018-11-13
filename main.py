# Z modulu flask naimportuje "Flask" a "g" tak, abychom je mohli
# používat v tomto programu
import os
from flask import Flask, g
# Stejně tak pro about_bp modul
import about_bp

import zavody_bp

import kdo_co_bp

import registrace_bp

bezciSobe = Flask(__name__)

# Stejně tak zaregistrujeme about_bp blueprint
bezciSobe.register_blueprint(about_bp.blueprint)
bezciSobe.register_blueprint(zavody_bp.blueprint)
bezciSobe.register_blueprint(kdo_co_bp.blueprint)
bezciSobe.register_blueprint(registrace_bp.blueprint)

# Zaregistruje funkci close_db() do naší aplikace jako funkci, která se má spustit,
# když se ukončuje naše aplikace

@bezciSobe.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        # Bezpečně ukončí spojení s naší databází
        g.db.close()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bezciSobe.run(host='0.0.0.0', port=port)

