from flask import Flask, render_template
from flask import make_response
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ =='__main__':
    app.run(debug=True)