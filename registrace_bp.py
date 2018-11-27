from flask import Blueprint, render_template, request, redirect,url_for
import db_funkce

blueprint = Blueprint('registrace_bp', __name__)
@blueprint.route('/registrace')
def show_registrace():
	return render_template('registrace.html', values={})

@blueprint.route('/registrace', methods=['POST'])
def add_new():
	result = request.form

	heslo = result.get("heslo")
	heslo_potvrzeni = result.get("heslo_potvrzeni")

	if not heslo == heslo_potvrzeni:
		# TODO: validace shody hesel
		pass

	if not result.get("skrtatko", "") == "ano":
		# pokud uzivatel nezaskrtne "skrtatko", bude
		# klic "skrtatko" v request.form chybet, proto
		# jsme zavolali .get s defaultni hodnotou ""
		pass

	id_uzivatele = db_funkce.registrace(
		result.get("jmeno"),
		result.get("prijmeni"),
		result.get("ulice"),
		result.get("mesto"),
		result.get("psc"),
		result.get("email"),
		result.get("telefon"),
		heslo,
		heslo_potvrzeni
	)

	if id_uzivatele:
		return render_template("potvrzeni_registrace.html")
		#return redirect(url_for("about_bp.show_index"))
	else:
		return render_template("registrace.html", values=result)
	#registrace(jmeno, prijmeni, ulice, mesto_obec, PSC, email, telefon, heslo)
	# Takhle funkce nám získá adresu (URL) pro funkci show() v tomhle blueprintu
    # tzn v tomhle konkrétním případě na adresu "/"
    #showUrl = url_for('prihlaseni_bp.show')
    	# Přesměuje uživatelův prohlížeč na adresu v showUrl, takže prohlížeč znovu
    	# načte tu úvodní stránku (tzn. že se znovu zavolá funkce show() výše), a ta
    	# znovu vypíše všechny záznamy z databáze, tentokrát i s tím záznamem, který
    	# jsme tam pravě vložili
    #return redirect(showUrl)

