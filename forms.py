from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField, SelectField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class PetForm(FlaskForm):
    peteval = TextAreaField("Evaluation", render_kw={"rows": 5}, validators=[InputRequired()])


class SearchForm(FlaskForm):
    pettype = SelectField(u"Pet Type", choices=[("Dog", "Dog"), ("Cat", "Cat"), ("Bird", "Bird"), ("Rabbit", "Rabbit")])
    gender = SelectField(u"Gender", choices=[("Male", "Male"), ("Female", "Female")])
    distance = SelectField(u"Distance", choices=[("25", "25"), ("50", "50"), ("75", "75"), ("100", "100")])
    location = StringField("Your Zip Code (Required)", validators=[InputRequired()])
