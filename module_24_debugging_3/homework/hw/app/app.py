import time
import random
from flask import Flask
import logging
from typing import Tuple

app = Flask(__name__)

app.config['DEBUG'] = True


@app.route('/one')
def the_first() -> Tuple[str, int]:
    logging.info('one')
    time.sleep(random.random() * 0.2)
    return 'ok', 201


@app.route('/two')
def the_second() -> Tuple[str, int]:
    logging.info('two')
    time.sleep(random.random() * 0.4)
    return 'ok', 202


@app.route('/three')
def the_third() -> Tuple[str, int]:
    logging.info('three')
    time.sleep(random.random() * 0.6)
    return 'ok', 203


@app.route('/four')
def the_fourth() -> Tuple[str, int]:
    logging.info('four')
    time.sleep(random.random() * 0.8)
    return 'ok', 204


@app.route('/five')
def the_fiveth() -> Tuple[str, int]:
    logging.info('five')
    time.sleep(random.random())
    return 'ok', 205


@app.route('/error')
def error() -> Tuple[str, int]:
    logging.info('error')
    a = 1 / 0
    return 'error', 500


if __name__ == "__main__":
    app.run(host='0.0.0.0')
