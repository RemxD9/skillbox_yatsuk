import logging
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired


app = Flask(__name__)
logger = logging.getLogger("Divider")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('stderr.txt', mode='w')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class DivisionForm(FlaskForm):
    a = IntegerField(validators=[InputRequired()])
    b = IntegerField(validators=[InputRequired()])


@app.route('/divide/', methods=['POST'])
def division():
    form = DivisionForm()

    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        logger.info(f"Form is valid, a = {a}, b = {b}")

        return f'a / b = {a / b:.2f}'

    logger.error(f"Form is not valid, error - {form.errors}")
    return f'Bad request', 400


@app.errorhandler(ZeroDivisionError)
def handle_exception(e: ZeroDivisionError):
    logger.exception("We are unable to divide by zero", exc_info=e)
    return f'We are unable to divide by zero', 400


if __name__ == '__main__':
    logger.info("Server has been started")
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
