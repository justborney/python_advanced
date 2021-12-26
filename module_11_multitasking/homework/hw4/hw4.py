import logging
import random
import threading
import time

TOTAL_TICKETS = 10
TOTAL_SOLD_TICKETS = 0
TOTAL_PLACES = 20

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Director(threading.Thread):

    def __init__(self, sellers_quantity, semaphore: threading.Semaphore):
        super(Director, self).__init__()
        self.quantity = sellers_quantity
        self.sem = semaphore
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS
        while TOTAL_SOLD_TICKETS + TOTAL_TICKETS < TOTAL_PLACES:
            if TOTAL_TICKETS <= self.quantity:
                if TOTAL_SOLD_TICKETS <= TOTAL_PLACES - TOTAL_TICKETS - self.quantity:
                    new_tickets_quantity = self.quantity
                else:
                    new_tickets_quantity = TOTAL_PLACES - TOTAL_SOLD_TICKETS - TOTAL_TICKETS
                TOTAL_TICKETS += new_tickets_quantity
                logger.info(f'{self.getName()} add {new_tickets_quantity} tickets;  {TOTAL_TICKETS} left')


class Seller(threading.Thread):

    def __init__(self, sellers_quantity, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.quantity = sellers_quantity
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        global TOTAL_SOLD_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                TOTAL_SOLD_TICKETS += 1
                logger.info(f'{self.getName()} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


def main():
    sellers_quantity = 4
    semaphore = threading.Semaphore()
    director = Director(sellers_quantity, semaphore)
    director.start()
    sellers = [director]
    for _ in range(sellers_quantity):
        seller = Seller(sellers_quantity, semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()

    logger.info(f'{TOTAL_SOLD_TICKETS} tickets sold of {TOTAL_PLACES} places')


if __name__ == '__main__':
    main()
