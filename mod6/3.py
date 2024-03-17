import json
import logging


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = msg.replace('"', "'")
        message = json.dumps(msg).replace('"', r'\"').replace('\n', r'\\n')
        return message, kwargs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}', datefmt='%H:%M:%S')
file_handler = logging.FileHandler('skillbox_json_messages.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
json_logger = JsonAdapter(logger, {})
json_logger.info('Пример JSON-логирования')
json_logger.warning('Сообщение с "двойными" кавычками')
json_logger.error('Много\nстрок\nв сообщении')
