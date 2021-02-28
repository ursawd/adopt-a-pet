from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField
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
