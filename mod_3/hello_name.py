from flask import Flask
from datetime import datetime


app = Flask(__name__)


weekdays_translator = {
    0: 'Хорошего понедельника!',
    1: 'Хорошего вторника!',
    2: 'Хорошей среды!',
    3: 'Хорошего четверга!',
    4: 'Хорошей пятницы!',
    5: 'Хорошей субботы!',
    6: 'Хорошего воскресенья!',
}


@app.route('/hello-world/<name>')
def hello_world(name):
    if 'хорошего' or 'хорошей' in name.lower():
        current_weekday = datetime.today().weekday()
        greeting = f'Привет, неизвестный пользователь! {weekdays_translator[current_weekday]}'
        return greeting
    else:
        current_weekday = datetime.today().weekday()
        greeting = f'Привет, {name}! {weekdays_translator[current_weekday]}'
        return greeting


if __name__ == '__main__':
    app.run(debug=True)
