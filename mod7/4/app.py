import logging
from utils import add, subtract
from logging.config import dictConfig
from logging_dict import config


logger = logging.getLogger()


def main():
    dictConfig(config)
    logger.info('Starting calculation')
    result_add = add(5, 3)
    logger.info('Result of addition: %s', result_add)
    result_subtract = subtract(10, 4)
    logger.info('Result of subtraction: %s', result_subtract)
    logger.info('Calculation completed')


if __name__ == "__main__":
    main()
