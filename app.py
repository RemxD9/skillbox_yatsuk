import datetime
import random
import re
import os
from flask import Flask

app = Flask(__name__)

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cars_string = ', '.join(cars_list)
cat_breeds = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

with open(BOOK_FILE, 'r', encoding='utf-8') as book:
    book_content = book.read()

words = [word for word in re.split(r'[.,;!?()\s\n\-]', book_content) if word]


@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'


@app.route('/cars')
def cars():
    return f'{cars_string}'


@app.route('/cats')
def cats():
    random_breed = random.choice(cat_breeds)
    return f'{random_breed}'


@app.route('/get_time/now')
def time_for_now():
    current_time = datetime.datetime.now()
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def future_time():
    current_time = datetime.datetime.now()
    one_hour = datetime.timedelta(hours=1)
    current_time_after_hour = current_time + one_hour
    return f'Точное время через час будет {current_time_after_hour}'


@app.route('/get_random_word')
def random_word():
    word = random.choice(words)
    return f'Случайное слово из романа Война и мир - {word}'


@app.route('/counter')
def counter():
    counter.visits += 1
    return f'Счетчик посещений страницы - {counter.visits}'


counter.visits = 0


if __name__ == '__main__':
    app.run(port=5555, debug=True)
