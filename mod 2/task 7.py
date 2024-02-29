from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

storage = {}


def is_valid_date(date_text, date_format='%Y%m%d'):
    try:
        datetime.strptime(date_text, date_format)
        return True
    except ValueError:
        return False


@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    try:
        if is_valid_date(date):
            year, month, day = int(date[:4]), int(date[4:6]), int(date[6:])
            expense = float(number)

            storage.setdefault(year, {}).setdefault(month, {'total': 0})
            storage[year][month].setdefault(day, 0)

            storage[year][month][day] += expense
            storage[year][month]['total'] += expense

            return f"Добавлена трата за {day}.{month}.{year}: {number} рублей, (наверное)"
        else:
            return f'Ошибка даты {date} не существует'

    except ValueError:
        return "неверный формат числа", 400
    except Exception as e:
        return f"Ошибка: {str(e)}", 500


@app.route('/calculate/<int:year>')
def calculate_year(year):
    try:
        total_expense = sum(month['total'] for month in storage.get(year, {}).values())
        return jsonify({'year': year, 'total expense': total_expense})

    except Exception as e:
        return f"Ошибка: {str(e)}", 500


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    try:
        # Получаем общую сумму затрат за месяц
        total_expense = storage.get(year, {}).get(month, {}).get('total', 0)
        return jsonify({'year': year, 'month': month, 'total expense': total_expense})

    except Exception as e:
        return f"Ошибка: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
