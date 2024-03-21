import logging
import logging_tree
from utils import add, subtract
from logging.config import dictConfig
from logging_dict import config


dictConfig(config)
logger = logging.getLogger(__name__)


def main():
    logger.info('Starting calculation')
    result_add = add(5, 3)
    logger.info('Result of addition: %s', result_add)
    result_subtract = subtract(10, 4)
    logger.info('Result of subtraction: %s', result_subtract)
    logger.info('Calculation completed')
    tree = logging_tree.tree()
    tree_str = '\n'.join([str(node) for node in tree])
    with open('logging_tree.txt', 'w') as f:
        f.write(tree_str)


if __name__ == "__main__":
    main()
