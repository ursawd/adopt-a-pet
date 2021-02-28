from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Pet
import requests, json
from libs.petlib import get_API_response
from forms import RegisterForm, LoginForm, PetForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt-a-pet"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension

app.config["SECRET_KEY"] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


@app.route("/")
def home():
    return render_template("home.html")
