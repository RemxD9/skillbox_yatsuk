import logging
from utils import add, subtract


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def main():
    logger.info('Starting calculation')
    result_add = add(5, 3)
    logger.info('Result of addition: %s', result_add)
    result_subtract = subtract(10, 4)
    logger.info('Result of subtraction: %s', result_subtract)
    logger.info('Calculation completed')


if __name__ == "__main__":
    main()
