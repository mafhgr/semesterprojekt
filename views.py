from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


transaktions_liste = []

# Pfad, um eine Transaktion hinzuzufügen
@views.route('/home', methods=['GET', 'POST'])
def transaktion_hinzufuegen():
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
        
    return render_template('home.html', user=current_user)

@views.route('/budget')
def budget():
    budgets = session.get('budgets', [])
    return render_template('budget.html', budgets=budgets, user=current_user)


@views.route('/submit_budget', methods=['POST'])
def submit_budget():
    month = request.form.get('month')
    category = request.form.get('category')
    amount = request.form.get('amount')
    
    new_budget = {'month': month, 'category': category, 'amount': amount}

    if 'budgets' not in session:
        session['budgets'] = []
    
    session['budgets'].append(new_budget)
    session.modified = True  # Stellt sicher, dass die Session aktualisiert wird

    return redirect(url_for('budget'), user=current_user)





@views.route('/transaktionsverlauf')
def transaktionsverlauf():
    return render_template('transaktionsverlauf.html', transaktionen=transaktions_liste, user=current_user)





@views.route('/berichte')
def berichte():
    return render_template('berichte.html', user=current_user)
