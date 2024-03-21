import logging
import flask.cli
from flask import Flask, request


app = Flask(__name__)


@app.route('/log', methods=['POST'])
def log():
    log_data = request.json
    print(log_data)
    return 'OK', 200


if __name__ == '__main__':
    flask.cli.show_server_banner = lambda *args: None
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='127.0.0.1', port=3000)
