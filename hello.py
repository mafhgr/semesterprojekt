from flask import Flask, render_template

app = Flask("Mein Semesterprojekt")

#Pfad, den der Benutzer aufruft
@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)