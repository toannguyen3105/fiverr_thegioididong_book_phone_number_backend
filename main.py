#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from queue import Queue
from threading import Thread
from time import time, sleep
from datetime import datetime

from constants.users import USERS, USER_TEST
from utils.download import buy_phone_number

users = USERS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            name, phone, identification_card, phone_number_to_buy, time_start = self.queue.get()
            try:
                buy_phone_number(name, phone, identification_card, phone_number_to_buy, time_start)
            finally:
                self.queue.task_done()


def main():
    ts = time()
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple

    for user in users:
        name = user["name"]
        phone = user["phone"]
        identification_card = user["identification_card"]
        phones_number_to_buy = user["phones_number_to_buy"]

        for phone_number_to_buy in phones_number_to_buy:
            logger.info('Queueing {}'.format(phone_number_to_buy))
            queue.put((name, phone, identification_card, phone_number_to_buy,
                       datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
        # Causes the main thread to wait for the queue to finish processing all the tasks
        queue.join()
        logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    while True:
        main()
        sleep(10)
