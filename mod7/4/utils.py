import logging


logger = logging.getLogger(__name__)


def add(x, y):
    logger.info('Adding %s and %s', x, y)
    return x + y


def subtract(x, y):
    logger.info('Subtracting %s from %s', y, x)
    return x - y
