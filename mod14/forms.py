from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from wtforms.validators import InputRequired


class MyForm(FlaskForm):
    title = StringField(validators=[InputRequired()])
    author = StringField(validators=[InputRequired()])
