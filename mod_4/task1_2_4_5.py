import subprocess
import shlex
from flask import Flask, request
from typing import List, Optional
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, NumberRange

app = Flask(__name__)


# Валидатор на классе для поля Phone
class PhoneValidator:
    def __init__(self, message=None):
        self.min_length = 1000000000
        self.max_length = 9999999999
        self.message = message

    def __call__(self, form: FlaskForm, field):
        if field.data is not None and not (self.min_length <= int(field.data) <= self.max_length):
            raise ValidationError(
                self.message or f'Field must be between {self.min_length} and {self.max_length}.')


# Валидатор в виде функции для поля Phone
def validator_for_phone(message=None):
    min_length = 1000000000
    max_length = 9999999999

    def _validator_for_phone(form: FlaskForm, field):
        if field.data is not None and not (min_length <= int(str(field.data)) <= max_length):
            raise ValidationError(message or f'Field must be between {min_length} and {max_length}')


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), PhoneValidator(message='Invalid phone number')])
    name = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    index = IntegerField(validators=[InputRequired(), NumberRange(min=0, message='Invalid index')])
    comment = StringField()


@app.route('/registration', methods=['POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f'successfully register {email} with phone: +7{phone}'

    return f'invalid input: {form.errors}', 400


@app.route('/uptime/', methods=['GET'])
def get_uptime():
    try:
        result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, text=True)
        uptime_output = result.stdout.strip()
        return f"Current uptime is {uptime_output}"
    except Exception as e:
        return f"Error getting uptime: {e}"


@app.route('/ps/', methods=['GET'])
def execute_ps():
    try:
        args: List[str] = request.args.getlist('arg')
        clean_args = [shlex.quote(arg) for arg in args]
        cmd = ['ps'] + clean_args
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        return f'<pre>{result.stdout}</pre>'
    except Exception as e:
        return f'Ошибка в исполнении команды ps: {e}'


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
