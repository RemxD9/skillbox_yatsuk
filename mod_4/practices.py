import datetime
from itertools import product
from flask import Flask, request
from typing import List, Optional


app = Flask(__name__)


def validate_array(array):
    validated_array = []
    for number in array:
        if number.isdigit():
            validated_array.append(number)
    return validated_array


def validate_number(number):
    try:
        isinstance(number, int)
        return True
    except ValueError:
        return False


def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False


def validate_prefixes(phone_prefix):
    return phone_prefix[:-1].isdigit() and phone_prefix[-1] == '*' and len(phone_prefix) <= 10


def validate_params(request):
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    cell_tower_id = request.args.get('cell_tower_id')
    protocol = request.args.get('protocol')
    phone_prefix = request.args.get('phone_prefix')

    if cell_tower_id and int(cell_tower_id) <= 0:
        return False

    if date_to and date_from:
        if not (validate_date(date_to) and validate_date(date_from) and date_from <= date_to):
            return False

    if protocol and protocol not in ['2G', '3G', '4G']:
        return False

    if phone_prefix and not validate_prefixes(phone_prefix):
        return False

    return True


@app.route('/search/', methods=['GET'])
def search():
    if validate_params(request):
        cell_towers_ids: List[int] = request.args.getlist('cell_tower_id', type=int)

        phone_prefixes: List[str] = request.args.getlist('phone_prefix')

        protocols: List[str] = request.args.getlist('protocol')

        signal_levels: Optional[float] = request.args.get('signal_level', type=float, default=None)

        date_from: Optional[str] = request.args.get('date_from', type=str, default=None)

        date_to: Optional[str] = request.args.get('date_to', type=str, default=None)

        return (
            f'Search for {cell_towers_ids}, Search criteria: <br>'
            f'Phone_prefixes: {phone_prefixes} <br>'
            f'protocols: {protocols} <br>'
            f'signal_levels: {signal_levels} <br>'
            f'date_from: {date_from}, date_to: {date_to}'
        )
    else:
        return f'Что-то не прошло валидацию', 400


@app.route('/math/', methods=['GET'])
def math():
    numbers: List[int] = request.args.getlist('numbers', type=int)

    summary = 0
    multiplication = 1
    for num in numbers:
        if not validate_number(num):
            continue
        summary += num
        multiplication *= num

    return (
        f'Сумма: {summary} <br>'
        f'Произведение: {multiplication}'
    )


@app.route('/combinearrays/', methods=['GET'])
def combine_arrays():

    first_array: List[int] = validate_array(request.args.getlist('array1'))
    second_array: List[int] = validate_array(request.args.getlist('array2'))

    if not first_array or not second_array:
        return 'Что-то пошло не так, скорее всего вы не включили в запрос какой-то массив', 400

    combinations = list(product(first_array, second_array))

    return f'Combinations: {combinations}'


@app.route('/closest_number/', methods=['GET'])
def closest_number():
    array: List[int] = validate_array(request.args.getlist('array', type=int))
    if validate_number(request.args.get('x', type=int)):
        number = request.args.get('x', type=int)

    close_number = min(array, key=lambda num: abs(num - number))

    return f'Ближайшее число из массива: {array} - {close_number}'


if __name__ == '__main__':
    app.run(debug=True)
