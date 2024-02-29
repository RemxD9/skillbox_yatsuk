import os.path

from flask import Flask
from datetime import datetime
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class ListConverter(BaseConverter):
    regex = r'-?\d*\.?\d+(?:\.\d+)?(?:/-?\d+(?:\.\d+)?)*'


weekdays_translator = {
    0: 'Хорошего понедельника',
    1: 'Хорошего вторника',
    2: 'Хорошей среды',
    3: 'Хорошего четверга',
    4: 'Хорошей пятницы',
    5: 'Хорошей субботы',
    6: 'Хорошего воскресенья',
}


@app.route('/hello-world/<name>')
def hello_world(name):
    current_weekday = datetime.today().weekday()
    greeting = f'Привет, {name}! {weekdays_translator[current_weekday]}!'
    return greeting


app.url_map.converters['path'] = ListConverter


@app.route('/max-number/<path:numbers>')
def max_number(numbers):
    numbers_list = list(map(float, numbers.split('/')))
    if numbers_list:
        max_num = max(numbers_list)
        result_type = int if max_num.is_integer() else float
        response = f'Максимальное переданное число {result_type(max_num)}'
    else:
        response = f'Список чисел пуст'

    return response


@app.route('/preview/<int:size>/<path:relative_path>')
def preview(size, relative_path):
    try:
        current_directory = os.getcwd()
        abs_path = os.path.join(current_directory, relative_path)

        with open(abs_path, 'r') as file:
            content = file.read(size)

        result_size = len(content)
        result_text = content.replace('\n', '<br>')

        return f'{abs_path} {result_size}<br>{result_text}'

    except Exception as e:
        return f"error {str(e)}", 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)
