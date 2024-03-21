import logging
from utils import add, subtract, configure_logger


logger = logging.getLogger(__name__)


def main():
    configure_logger()
    logger.info('Starting calculation')
    result_add = add(5, 3)
    logger.info('Result of addition: %s', result_add)
    result_subtract = subtract(10, 4)
    logger.info('Result of subtraction: %s', result_subtract)
    logger.info('Calculation completed')


if __name__ == "__main__":
    main()