# Z modulu flask naimportuje "Flask" a "g" tak, abychom je mohli
# používat v tomto programu
from flask import Flask, g
# Stejně tak pro about_bp modul
import about_bp

# Vytvoří novou Flask aplikaci a uloží ji do proměnné "kateApp"
bezciSobe = Flask(__name__)

# Stejně tak zaregistrujeme about_bp blueprint
bezciSobe.register_blueprint(about_bp.blueprint)

# Zaregistruje funkci close_db() do naší aplikace jako funkci, která se má spustit,
# když se ukončuje naše aplikace
'''
@bezciSobe.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        # Bezpečně ukončí spojení s naší databází
        g.sqlite_db.close()
'''