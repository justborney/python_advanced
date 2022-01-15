import logging.config
import sys
import threading
import time
from threading import Lock

import requests

from log_conf import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger("custom_logger")

LOCK = Lock()


class Writer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        time_start = time.time()
        while time.time() - time_start < 20:
            time.sleep(1)
            time_stamp = int(time.time())
            request_text = 'https://showcase.api.linx.twenty57.net/UnixTime/fromunix?timestamp=' + str(time_stamp)
            res = requests.get(request_text)
            result = f'{threading.current_thread().getName()} / {sys.argv[0]} - {res.text[1:-1]}'
            with LOCK:
                logger.info(result)


def log_writers():
    writers_quantity = 10
    writers = []

    for _ in range(writers_quantity):
        time.sleep(1)
        writer = Writer()
        writer.start()
        writers.append(writer)

    for writer in writers:
        writer.join()


if __name__ == '__main__':
    log_writers()
