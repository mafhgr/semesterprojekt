from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    transaktionen = load_transactions()
    anzahl_transaktionen = len(transaktionen)
    gesamtvolumen_ausgaben = sum(float(t['Betrag']) for t in transaktionen if t['Transaktionsart'] == 'Ausgabe')
    gesamtvolumen_einnahmen = sum(float(t['Betrag']) for t in transaktionen if t['Transaktionsart'] == 'Einnahme')

    return render_template('dashboard.html', anzahl_transaktionen=anzahl_transaktionen, 
                           gesamtvolumen_ausgaben=gesamtvolumen_ausgaben,
                           gesamtvolumen_einnahmen=gesamtvolumen_einnahmen)





def save_transactions(transactions):
    with open('semesterprojekt/transactions.json', 'w') as file:
        json.dump(transactions, file, indent=4)

def load_transactions():
    try:
        with open('semesterprojekt/transactions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/transaktion_hinzufuegen', methods=['GET', 'POST'])
def transaktion_hinzufuegen():
    if request.method == 'POST':
        transaktion = request.form['transaktion']
        transaktionsart = request.form['transaktionsart']
        betrag = request.form['betrag']
        kategorie = request.form['kategorie']
        datum = request.form['datum']
        bemerkungen = request.form['bemerkungen']

        transaktion_data = {
            'Transaktion': transaktion,
            'Transaktionsart': transaktionsart,
            'Betrag': betrag,
            'Kategorie': kategorie,
            'Datum': datum,
            'Bemerkungen': bemerkungen
        }

        transaktionen = load_transactions()
        transaktionen.append(transaktion_data)
        save_transactions(transaktionen)

        return redirect(url_for('transaktion_hinzufuegen'))

    return render_template('transaktion_hinzufuegen.html')

@app.route('/transaktionsverlauf')
def transaktionsverlauf():
    transaktionen = load_transactions()
    for transaktion in transaktionen:
        transaktion['Betrag'] = float(transaktion['Betrag'])
    return render_template('transaktionsverlauf.html', transaktionen=transaktionen)


# Funktionen für Budgets
def save_budgets(budgets):
    with open('semesterprojekt/budgets.json', 'w') as file:
        json.dump(budgets, file, indent=4)

def load_budgets():
    try:
        with open('semesterprojekt/budgets.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        month = request.form.get('month')
        category = request.form.get('category')
        amount = request.form.get('amount')

        new_budget = {'month': month, 'category': category, 'amount': amount}
        
        budgets = load_budgets()
        budgets.append(new_budget)
        save_budgets(budgets)

        return redirect(url_for('budget'))

    budgets = load_budgets()
    return render_template('budget.html', budgets=budgets)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
