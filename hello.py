from flask import Flask, render_template

app = Flask("Mein Semesterprojekt")

#Pfad, den der Benutzer aufruft
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/transaktionsverlauf')
def transaktionsverlauf():
    return render_template('transaktionsverlauf.html')

@app.route('/berichte')
def berichte():
    return render_template('berichte.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)