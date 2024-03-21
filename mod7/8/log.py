import logging
import requests
import json


class FlaskHTTPHandler(logging.Handler):
    def __init__(self, url, method='POST', headers=None, body_template=None):
        super().__init__()
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.body_template = body_template

    def emit(self, record):
        log_entry = self.format(record)
        headers = {'Content-Type': 'application/json'}
        headers.update(self.headers)
        body = self.body_template.format(log_entry=log_entry) if self.body_template else log_entry
        requests.request(self.method, self.url, headers=headers, data=json.dumps(body))


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = FlaskHTTPHandler(url='http://127.0.0.1:3000/log')
logger.addHandler(handler)

logger.info('This is a test log message')
