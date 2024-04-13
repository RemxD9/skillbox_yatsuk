from flask import Flask
import time

app = Flask(__name__)


@app.route('/timestamp/<int:timestamp>')
def get_timestamp(timestamp):
    return str(int(time.time()))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
