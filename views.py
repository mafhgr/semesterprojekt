from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

'''

transaktions_liste = []

# Pfad, um eine Transaktion hinzuzufügen
@views.route('/dashboard', methods=['GET', 'POST'])
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

@views.route('/budget')
def budget():
    budgets = session.get('budgets', [])
    return render_template('budget.html', budgets=budgets)


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

    return redirect(url_for('budget'))





@views.route('/transaktionsverlauf')
def transaktionsverlauf():
    return render_template('transaktionsverlauf.html', transaktionen=transaktions_liste)




@views.route('/berichte')
def berichte():
    return render_template('berichte.html')
'''