import time

from flask import Flask, jsonify

application = Flask(__name__)


@application.route('/hello')
@application.route('/hello/<username>')
def hello_world(username='username'):
    return jsonify(message='hello', name=username)


@application.route('/my_app')
def my_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']


@application.route('/my_app_2')
def my_app_2():
    return jsonify('Result of my_app_2')


@application.route('/long_task')
def long_task():
    time.sleep(200)
    return jsonify(message='We did it!')
