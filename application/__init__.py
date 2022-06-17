from flask import Flask, render_template

app = Flask(__name__)

users = ['Malik Piara', 'John Snow', 'Clark Kent']


@app.route("/")
def hello_world():
    return render_template('hello.html')


@app.route("/join")
def signup():
    return render_template('signup.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/people")
def people():
    return render_template('people.html', users=users)
