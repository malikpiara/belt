import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

load_dotenv()
app = Flask(__name__)


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # PyMongo Configuration
    app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")
    mongo = PyMongo(app)


app.config.from_object(Config)

db = Config.mongo.db


# Models
def create_user(email_address, first_name, last_name, password):
    hashed_pass = generate_password_hash(
        password)
    db.users.insert_one(
        {
            "email": email_address,
            "first_name": first_name,
            "last_name": last_name,
            "password": hashed_pass,
            "account_status": "active",
        })


def get_users():
    users = []
    for user in db.users.find(
        {
            "_id": {"$exists": True}
        }
    ):
        entry = {
            "_id": user["_id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "location": user["location"],
            "can_help_with": user["can_help_with"]
        }

        users.append(entry)
    return users


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
    users = get_users()
    return render_template('people.html', users=users)
