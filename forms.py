from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

s = "You must fill all the fills"


class RegisterForm(FlaskForm):
    username = StringField(
        "Enter your name",
        validators=[DataRequired(message=s)],
    )
    password = PasswordField(
        "Enter your password", validators=[DataRequired(message=s)]
    )
    repeat = PasswordField(
        "Repeat your password",
        validators=[
            DataRequired(message=s),
            EqualTo("password", message="The passwords don't match"),
        ],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired(message=s)])

    password = PasswordField(
        "Enter your password", validators=[DataRequired(message=s)]
    )

    remember = BooleanField("Remember it?", default=False)

    submit = SubmitField("Login")
