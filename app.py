from flask import Flask, render_template, request, session, redirect, url_for
import json
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from uuid import uuid4


# Initialisiert die Flask-Anwendung
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
# Setzt den geheimen Schlüssel für Sessions

# Route zur Startseite, die das Dashboard-Template rendert
@app.route('/')
def home():
    return render_template('dashboard.html')

# Dashboard-Route, die Transaktionsdaten lädt und an das Template weitergibt
@app.route('/dashboard')
def dashboard():
    transaktionen = load_transactions()
    anzahl_transaktionen = len(transaktionen)
    gesamtvolumen_ausgaben = sum(
        float(t['Betrag']) for t in transaktionen if t['Transaktionsart'] == 'Ausgabe')
    gesamtvolumen_einnahmen = sum(
        float(t['Betrag']) for t in transaktionen if t['Transaktionsart'] == 'Einnahme')
    
    budgets = load_budgets()
    if budgets:
        gesamtbudget = sum(float(budget['amount']) for budget in budgets)
    else:
        gesamtbudget = 0

    plot_url_ausgaben = kategorie_spezifische_ausgaben(transaktionen)
    plot_url_einnahmen = einnahmen_pro_kategorie(transaktionen)

    return render_template('dashboard.html', gesamtbudget=gesamtbudget, anzahl_transaktionen=anzahl_transaktionen, gesamtvolumen_ausgaben=gesamtvolumen_ausgaben, gesamtvolumen_einnahmen=gesamtvolumen_einnahmen, plot_url_ausgaben=plot_url_ausgaben, plot_url_einnahmen=plot_url_einnahmen)


# Funktionen für das Erstellen von Diagrammen zu Ausgaben und Einnahmen
def kategorie_spezifische_ausgaben(transaktionen):
    kategorien = set(t['Kategorie'] for t in transaktionen)
    ausgaben_pro_kategorie = {k: 0 for k in kategorien}

    for t in transaktionen:
        if t['Transaktionsart'] == 'Ausgabe':
            ausgaben_pro_kategorie[t['Kategorie']] += float(t['Betrag'])

    kategorien = list(ausgaben_pro_kategorie.keys())
    ausgaben = [ausgaben_pro_kategorie[k] for k in kategorien]

    fig, ax = plt.subplots()
    ax.bar(kategorien, ausgaben)
    ax.set_xlabel('Kategorien')
    ax.set_ylabel('Ausgaben')
    ax.set_title('Ausgaben pro Kategorie')

    # Konvertierung in ein Bildformat, das im HTML-Template angezeigt werden kann
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url_ausgaben = base64.b64encode(img.getvalue()).decode()

    return plot_url_ausgaben


def einnahmen_pro_kategorie(transaktionen):
    kategorien = set(t['Kategorie'] for t in transaktionen)
    einnahmen_pro_kategorie = {k: 0 for k in kategorien}

    for t in transaktionen:
        if t['Transaktionsart'] == 'Einnahme':
            einnahmen_pro_kategorie[t['Kategorie']] += float(t['Betrag'])

    kategorien = list(einnahmen_pro_kategorie.keys())
    einnahmen = [einnahmen_pro_kategorie[k] for k in kategorien]

    fig, ax = plt.subplots()
    ax.bar(kategorien, einnahmen, color='green')
    ax.set_xlabel('Kategorien')
    ax.set_ylabel('Einnahmen')
    ax.set_title('Einnahmen pro Kategorie')

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url_einnahmen = base64.b64encode(img.getvalue()).decode('utf-8')

    return plot_url_einnahmen

# Funktionen zum Speichern und Laden von Transaktionen
def save_transactions(transactions):
    with open('/transactions.json', 'w') as file:
        json.dump(transactions, file, indent=4)


def load_transactions():
    try:
        with open('/transactions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

 # Route zum Hinzufügen einer Transaktion
@app.route('/transaktion_hinzufuegen', methods=['GET', 'POST'])
def transaktion_hinzufuegen():
    if request.method == 'POST':
        transaktion = request.form['transaktion']
        transaktionsart = request.form['transaktionsart']
        betrag = request.form['betrag']
        kategorie = request.form['kategorie']
        datum = request.form['datum']
        bemerkungen = request.form['bemerkungen']

        transaktionen = load_transactions()
        neue_id = len(transaktionen) + 1
        transaktion_data = {
            'id': neue_id,
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

        return redirect(url_for('transaktionsverlauf'))

    return render_template('transaktion_hinzufuegen.html')

 # Route zum Löschen einer Transaktion
@app.route('/delete_transaktion/<int:transaktion_id>')
def delete_transaktion(transaktion_id):
    transaktionen = load_transactions()
    transaktionen = [t for t in transaktionen if t.get('id') != transaktion_id]
    save_transactions(transaktionen)
    return redirect(url_for('transaktionsverlauf'))

# Route zum Anzeigen des Transaktionsverlaufs
@app.route('/transaktionsverlauf')
def transaktionsverlauf():
    transaktionen = load_transactions()
    for transaktion in transaktionen:
        transaktion['Betrag'] = float(transaktion['Betrag'])
    return render_template('transaktionsverlauf.html', transaktionen=transaktionen)


# Funktionen für Budgets
def save_budgets(budgets):
    with open('/budgets.json', 'w') as file:
        json.dump(budgets, file, indent=4)


def load_budgets():
    try:
        with open('/budgets.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Route zur Budgetverwaltung
@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        month = request.form.get('month')
        category = request.form.get('category')
        amount = request.form.get('amount')
        budgets = load_budgets()

        new_budget = {
            'id': str(uuid4()),  # Assign a unique UUID
            'month': month,
            'category': category,
            'amount': amount
        }
        budgets.append(new_budget)
        save_budgets(budgets)
        return redirect(url_for('budget'))

    budgets = load_budgets()
    return render_template('budget.html', budgets=budgets)

# Route zum Löschen eines Budgets
@app.route('/delete_budget/<budget_id>')
def delete_budget(budget_id):
    budgets = load_budgets()
    budgets = [budget for budget in budgets if budget['id'] != budget_id]
    save_budgets(budgets)
    return redirect(url_for('budget'))


# Fehlerhafte URL wird auf die Startseite umgeleitet
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('dashboard'))


# Startet die Anwendung im Debug-Modus auf Port 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)
