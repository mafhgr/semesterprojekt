from flask import Flask, render_template

app = Flask("Mein Se")

#Pfad, den der Benutzer aufruft
@app.route('/')
def index():
    card1 = {
        'title': 'Karte 1',
        'content': 'Das ist der Inhalt der ersten Karte'
    }
    card2 = {
        'title': 'Karte 2',
        'content': 'Das ist der Inhalt der zweiten Karte'
    }
    return render_template('index.html', card1=card1, card2=card2)



if __name__ == '__main__':
    app.run(debug=True, port=5000)