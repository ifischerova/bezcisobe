from flask import Blueprint, render_template, request, redirect,url_for
import db_funkce

blueprint = Blueprint('registrace_bp', __name__)
@blueprint.route('/registrace') # , methods = ['POST'])
def show_registrace():
	#if request.method == 'POST':
      #result = request.form
	return render_template('registrace.html',values={})

@blueprint.route('/registrace', methods=['POST'])
def add_new():
	result = request.form
	db_funkce.registrace(**result)
	# nastav podle toho, jestli se registrace povedla nebo to upadlo
	success = True

	if success:
		return redirect(url_for("about_bp.show_index"))
	else:
		return render_template("registrace.html", values=result)
	#registrace(jmeno, prijmeni, ulice, mesto_obec, PSC, email, telefon, heslo)
	# Takhle funkce nám získá adresu (URL) pro funkci show() v tomhle blueprintu
    	# tzn v tomhle konkrétním případě na adresu "/"
    #showUrl = url_for('registrace_bp.show')
    	# Přesměuje uživatelův prohlížeč na adresu v showUrl, takže prohlížeč znovu
    	# načte tu úvodní stránku (tzn. že se znovu zavolá funkce show() výše), a ta
    	# znovu vypíše všechny záznamy z databáze, tentokrát i s tím záznamem, který
    	# jsme tam pravě vložili
    #return redirect(showUrl)

