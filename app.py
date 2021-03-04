from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Pet
from libs.petlib import get_API_response, get_random_pet
from forms import RegisterForm, LoginForm, PetForm, SearchForm
import requests, json, html

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt-a-pet"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension

app.config["SECRET_KEY"] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# ######################################################################
#
@app.route("/")
def home():
    # get random pet for pet to the day display
    response = get_random_pet()
    session["response"] = response

    return render_template("home.html", response=response)


# ######################################################################
#
@app.route("/login", methods=["GET", "POST"])
def user_login():
    """ Login user """

    # create form
    form = LoginForm()
    # check if valid  submitted, this check false if GET
    if form.validate_on_submit():
        # get form values
        username = form.username.data
        password = form.password.data
        # check username and hashed password to see if in db
        user = User.login(username, password)
        # if username and password match, store username, see to protected page(s)
        if user:  # contains found user object or False
            # set session data key "username" to contain logged in username
            session["username"] = user.username
            return redirect("/search")
        else:
            # inform user of bad input
            form.username.errors = ["Invalid username / password"]
    # here if either GET route or bad input to login form
    return render_template("login.html", form=form)


# ######################################################################
#
@app.route("/register", methods=["GET", "POST"])
def register():
    """show registration form
    process registration form
    add user to db
    """
    # create form
    form = RegisterForm()
    # check if valid  submitted, this check false if GET
    if form.validate_on_submit():
        # get form values
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        # ! check for username in database
        # generate hashed password with bcrypt
        # return User instance with just username and hashed password
        user = User.register(username, password)
        # add rest of data to User instance
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        # add User instance to db
        db.session.add(user)
        db.session.commit()

        # store username in session data
        # check username and hashed password to see if in db
        user = User.login(username, password)
        # if username and password match, store username, see to protected page(s)
        if user:  # contains found user object or False
            session["username"] = user.username

        # provide user confirmation registration successful
        flash(f" Added user {username}")  # todo not implemented yet
        # redirect to protected page(s)
        return redirect("/search")
    else:  # if here: validation error or GET request
        return render_template("register.html", form=form)


# ######################################################################
#
@app.route("/logout")
def logout():
    """Log out user"""
    if "username" in session:
        session.pop("username")
        session.pop("response")
    return redirect("/")


# ######################################################################
#
@app.route("/search", methods=["GET", "POST"])
def search():
    """Display search options"""

    # create form
    form = SearchForm()

    # # check if valid  submitted, this check false if GET
    if form.validate_on_submit():

        # get form values
        pet_type = form.pettype.data
        gender = form.gender.data
        distance = form.distance.data
        location = form.location.data

        params = (
            ("type", pet_type),
            ("gender", gender),
            ("distance", distance),
            ("location", location),
        )
        url = "https://api.petfinder.com/v2/animals"
        resp = get_API_response(url, params)

        return render_template("displaypets.html", resp=resp)
    return render_template("search.html", response=session["response"], form=form)


# ######################################################################
#
