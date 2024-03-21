import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def add(x, y):
    logger.info('Adding %s and %s', x, y)
    return x + y


def subtract(x, y):
    logger.info('Subtracting %s from %s', y, x)
    return x - y