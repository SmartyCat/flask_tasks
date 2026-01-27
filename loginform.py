from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired


class RegisterForm(FlaskForm):
    username = StringField(
        "Enter your username", validators=[DataRequired(), Length(min=4)]
    )
    password = PasswordField(
        "Enter your password", validators=[DataRequired(), Length(min=4, max=12)]
    )
    check_password = PasswordField(
        "Repeat your password", validators=[DataRequired(), Length(min=4, max=12)]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(
        "Enter your username", validators=[DataRequired(), Length(min=4)]
    )
    password = PasswordField(
        "Enter your password", validators=[DataRequired(), Length(min=4, max=12)]
    )
    submit = SubmitField("Enter")
