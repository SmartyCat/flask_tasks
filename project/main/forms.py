from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class Form(FlaskForm):
    username = StringField("Enter your username")
    submit = SubmitField("Enter")
