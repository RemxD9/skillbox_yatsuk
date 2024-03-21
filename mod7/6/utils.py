import logging


utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.INFO)
utils_handler = logging.FileHandler('utils.log')
utils_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
utils_handler.setFormatter(formatter)
utils_logger.addHandler(utils_handler)


def add(x, y):
    utils_logger.info('Adding %s and %s', x, y)
    return x + y


def subtract(x, y):
    utils_logger.info('Subtracting %s from %s', y, x)
    return x - y
