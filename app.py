from flask import Flask, render_template, redirect, url_for, request, session, flash
import json

app = Flask("Mein Semesterprojekt")


#Dashboard
@app.route('/')
def index():
    return render_template('dashboard.html')

transaktions_liste = []

# Pfad, um eine Transaktion hinzuzufügen
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Daten aus dem Formular abrufen
        transaktion = request.form['transaktion']
        transaktionsart = request.form['transaktionsart']
        betrag = request.form['betrag']
        kategorie = request.form['kategorie']
        datum = request.form['datum']
        bemerkungen = request.form['bemerkungen']

        # Eine JSON-Darstellung der Transaktion erstellen
        transaktion_data = {
            'Transaktion': transaktion,
            'Transaktionsart': transaktionsart,
            'Betrag': betrag,
            'Kategorie': kategorie,
            'Datum': datum,
            'Bemerkungen': bemerkungen
        }

        # Die Transaktionsdaten zur Liste hinzufügen
        transaktions_liste.append(transaktion_data)
        
    return render_template('dashboard.html')

@app.route('/budget')
def budget():
    budgets = session.get('budgets', [])
    return render_template('budget.html', budgets=budgets)


@app.route('/submit_budget', methods=['POST'])
def submit_budget():
    month = request.form.get('month')
    category = request.form.get('category')
    amount = request.form.get('amount')
    
    new_budget = {'month': month, 'category': category, 'amount': amount}

    if 'budgets' not in session:
        session['budgets'] = []
    
    session['budgets'].append(new_budget)
    session.modified = True  # Stellt sicher, dass die Session aktualisiert wird

    return redirect(url_for('budget'))





@app.route('/transaktionsverlauf')
def transaktionsverlauf():
    return render_template('transaktionsverlauf.html', transaktionen=transaktions_liste)




@app.route('/berichte')
def berichte():
    return render_template('berichte.html')



if __name__ == '__main__':
    app.secret_key = 'dein_geheimer_schluessel'
    app.run(debug=True, port=5000)