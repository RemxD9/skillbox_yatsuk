import logging
import threading
import random
import time

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


class Fork:
    def __enter__(self):
        logger.info('Fork is acquired')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('Fork is released')


class Philosopher(threading.Thread):
    running = True

    def __init__(self, left_fork: Fork, right_fork: Fork):
        super().__init__()
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while self.running:
            logger.info(f'Philosopher {self.getName()} start thinking.')
            time.sleep(random.randint(1, 10))
            logger.info(f'Philosopher {self.getName()} is hungry.')
            with self.left_fork, self.right_fork:
                self.dining()

    def dining(self):
        logger.info(f'Philosopher {self.getName()} starts eating.')
        time.sleep(random.randint(1, 10))
        logger.info(f'Philosopher {self.getName()} finishes eating and leaves to think.')


def main():
    forks = [Fork() for _ in range(5)]
    philosophers = [
        Philosopher(forks[i % 5], forks[(i + 1) % 5])
        for i in range(5)
    ]
    Philosopher.running = True
    for p in philosophers:
        p.start()
    time.sleep(200)
    Philosopher.running = False
    logger.info("Now we're finishing.")
    return


if __name__ == "__main__":
    main()
