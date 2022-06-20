from crypt import methods
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError, HiddenField, PasswordField, EmailField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, EqualTo, URL

load_dotenv()
app = Flask(__name__)


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # PyMongo Configuration
    app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")
    mongo = PyMongo(app)


app.config.from_object(Config)

db = Config.mongo.db

# Start of Forms


class SignUpForm(FlaskForm):
    first_name = StringField("Type your first name",
                             validators=([DataRequired()]))
    last_name = StringField("Type your last name",
                            validators=([DataRequired()]))
    location = StringField("Type your current location",
                           validators=([DataRequired()]))
    description = StringField(
        u'What can you do for the family?', widget=TextArea())
    email = EmailField("Type your email", validators=[
        DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo(
        "password2", message="Passwords must match.")])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Join Belt")

    def validate_email_address(self, field):
        email_address = field.data
        if find_user_by_email(email=email_address):
            #flash("Email already registered.")
            raise ValidationError('Email already registered.')


class SignIn(FlaskForm):
    email_address = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password")
    submit = SubmitField("Login")

# Models


def find_user_by_email(email):
    return db.users.find_one(
        {
            "email": email
        }
    )


def create_user(first_name, last_name, location, can_help_with, email_address, password):
    hashed_pass = generate_password_hash(
        password)
    db.users.insert_one(
        {
            "first_name": first_name,
            "last_name": last_name,
            "location": location,
            "can_help_with": can_help_with,
            "email": email_address,
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


@app.route("/join", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():

        create_user(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    location=form.location.data,
                    can_help_with=form.description.data,
                    email_address=form.email.data,
                    password=form.password.data
                    )

        return redirect(url_for('people'))

    return render_template('signup.html', form=form)


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/people")
def people():
    users = get_users()
    return render_template('people.html', users=users)
