import logging
import random
import threading
import time

TOTAL_TICKETS = 10
THRESHOLD = 1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, tickets_left: threading.Event):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        self.tickets_left = tickets_left
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one; {TOTAL_TICKETS} left')
                if TOTAL_TICKETS == THRESHOLD:
                    self.tickets_left.set()

        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, tickets_left: threading.Event):
        super().__init__()
        self.sem = semaphore
        self.tickets_left = tickets_left
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS
        while True:
            self.tickets_left.wait()
            with self.sem:
                if TOTAL_TICKETS <= THRESHOLD:
                    logger.info(f'Director is printing more tickets')
                    TOTAL_TICKETS += 6
                    logger.info(f'Director added 6 more tickets; Total tickets now: {TOTAL_TICKETS}')
                    self.tickets_left.clear()
                else:
                    break

        logger.info(f'Director finished')


def main():
    semaphore = threading.Semaphore()
    tickets_left = threading.Event()

    sellers = [Seller(semaphore, tickets_left) for _ in range(3)]
    director = Director(semaphore, tickets_left)

    for seller in sellers:
        seller.start()
    director.start()

    for seller in sellers:
        seller.join()
    director.join()


if __name__ == '__main__':
    logger.info('Start')
    main()
