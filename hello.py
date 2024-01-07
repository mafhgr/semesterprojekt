from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask("Mein Semesterprojekt")

#Pfad, den der Benutzer aufruft
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

transaktions_liste = []

# Pfad, um eine Transaktion hinzuzufügen
@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        # Daten aus dem Formular abrufen
        transaktion = request.form['transaktion']
        kosten = request.form['kosten']
        kategorie = request.form['kategorie']
        datum = request.form['datum']
        bemerkungen = request.form['bemerkungen']

        # Eine JSON-Darstellung der Transaktion erstellen
        transaktion_data = {
            'Transaktion': transaktion,
            'Kosten': kosten,
            'Kategorie': kategorie,
            'Datum': datum,
            'Bemerkungen': bemerkungen
        }

        # Die Transaktionsdaten zur Liste hinzufügen
        transaktions_liste.append(transaktion_data)
        

    return render_template('budget.html')


@app.route('/transaktionsverlauf')
def transaktionsverlauf():
    return render_template('transaktionsverlauf.html', transaktionen=transaktions_liste)

@app.route('/berichte')
def berichte():
    return render_template('berichte.html')


if __name__ == '__main__':
    app.secret_key = 'dein_geheimer_schluessel'
    app.run(debug=True, port=5000)