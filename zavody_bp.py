# Z flasku naimportuje spoustu různých funkcí, které budeme potřebovat
from flask import Blueprint, render_template, request, flash, abort
import db_funkce
import fce_zavody

blueprint = Blueprint('zavody_bp', __name__)

# Zaregistruje funkci show_about() jako funkci, kterou má Flask zavolat, když 
# uživatel otevře v prohlížeči stránku "/zavody"
@blueprint.route('/zavody/')
def show_zavody():
    # Zavolá funkci render_template(), která vezme template about.html a
    # vygeneruje výsledné HTML, které vrátí jako výsledek z téhle funkce zpátky
    # do Fasku, a ten ji pošle k uživateli do prohlížeče.
    datum_zavodu = request.args.get('datum_zavodu', default = '', type = str)
    id_zavod = request.args.get('id_zavod', default = 0, type = int)

    nabidka_spolujizdy = []
    if datum_zavodu:
        zavody = fce_zavody.zavody_dle_datumu(datum_zavodu)
        if zavody == []:
            flash ('Pro tento den není v databázi žádný závod.', "warning")
            zavody = db_funkce.zavody()
    else:
        zavody = db_funkce.zavody()
    if id_zavod:
        nabidka_spolujizdy = db_funkce.nabidky_spolujizdy(id_zavod)

    return render_template('zavody.html', zavody=zavody, datum_zavodu=datum_zavodu, id_vybraneho=id_zavod, nabidka_spolujizdy=nabidka_spolujizdy)
