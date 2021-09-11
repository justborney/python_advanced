import datetime
import random

from flask import Flask

app = Flask(__name__)

counter = 0


@app.route('/counter')
def counter_func():
    global counter
    counter += 1
    return 'This page was opened {0} times'.format(counter)


@app.route('/hello_world')
def hello_world_func():
    return 'Привет, мир!'


@app.route('/cars')
def cars_func():
    return 'Chevrolet, Renault, Ford, Lada'


@app.route('/cats')
def cats_func():
    return random.choice(['корниш рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин'])


@app.route('/get_time/now')
def get_time_now_func():
    return 'Точное время {current_time}'.format(current_time=datetime.datetime.now().time())


@app.route('/get_time/future')
def get_time_future_func():
    return 'Точное время через час будет {current_time_after_hour}'.format(
        current_time_after_hour=(datetime.datetime.now() + datetime.timedelta(hours=1)).time())


@app.route('/get_random_word')
def get_random_word_func():
    with open('module_01_flask/homework/war_and_peace.txt', 'r', encoding='utf-8') as war_and_peace_text:
        all_words = war_and_peace_text.read().split()
    return random.choice(all_words)
