import logging


logger = logging.getLogger(__name__)


def configure_logger():
    formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    info_handler = logging.FileHandler('calc_info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    root_logger.addHandler(info_handler)


def add(x, y):
    logger.info('Adding %s and %s', x, y)
    return x + y


def subtract(x, y):
    logger.info('Subtracting %s from %s', y, x)
    return x - y
