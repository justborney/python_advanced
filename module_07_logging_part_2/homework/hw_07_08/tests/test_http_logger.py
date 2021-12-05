import datetime
import os
import subprocess
import time
import unittest
from pathlib import Path

from module_07_logging_part_2.homework.hw_07_08.log_server import app

correct_data = {'name': 'http_logger', 'msg': 'Starting the app', 'args': '()',
                'levelname': 'DEBUG', 'levelno': '10',
                'pathname': '/PycharmProjects/python_advanced/module_07_logging_part_2/homework/hw_07.08/test_app.py',
                'filename': 'test_app.py', 'module': 'my_app', 'exc_info': 'None',
                'exc_text': 'None', 'stack_info': 'None',
                'lineno': '10', 'funcName': 'my_app_for_http_handler',
                'created': '1638054651.9576426',
                'msecs': '957.6425552368164', 'relativeCreated': '17.339706420898438',
                'thread': '140096086685504',
                'threadName': 'MainThread', 'processName': 'MainProcess',
                'process': '9238', 'message': 'Starting the app',
                'asctime': '2021-11-28 02:10:51,957'}

incorrect_data = {'msg': 'Starting the app', 'args': '()',
                  'levelno': '10',
                  'pathname': '/PycharmProjects/python_advanced/module_07_logging_part_2/homework/hw_07.08/test_app.py',
                  'filename': 'test_app.py', 'module': 'my_app', 'exc_info': 'None',
                  'exc_text': 'None', 'stack_info': 'None',
                  'funcName': 'my_app_for_http_handler',
                  'created': '1638054651.9576426',
                  'msecs': '957.6425552368164', 'relativeCreated': '17.339706420898438',
                  'thread': '140096086685504',
                  'threadName': 'MainThread', 'processName': 'MainProcess',
                  'process': '9238', 'message': 'Starting the app',
                  'asctime': '2021-11-28 02:10:51,957'}


class TestHTTPCustomLogger(unittest.TestCase):
    def test_server_working(self):
        result = app.test_client().post("http://localhost:5555/logger", data=correct_data)
        self.assertEqual(200, result.status_code)
        self.assertEqual(b'OK', result.data)

    def test_server_can_write_data(self):
        app.test_client().post("http://localhost:5555/logger", data=correct_data)
        with open('my_app.log', 'r') as log_file:
            result = log_file.readlines()[-1]
        self.assertTrue('server_logger | DEBUG | http_logger | 2021-11-28 02:10:51,957 | 10 | Starting the app',
                        result)

    def test_server_can_not_handle_incorrect_data(self):
        result = app.test_client().post("http://localhost:5555/logger", data=incorrect_data)
        self.assertEqual(400, result.status_code)
        self.assertEqual(b'Bad request', result.data)

    def test_correct_app_and_server_working(self):
        with subprocess.Popen(['python', 'log_server.py'], cwd=Path(os.getcwd()).parents[0]) as server:
            time.sleep(1)
            with subprocess.Popen(['python', 'test_app.py'], stdout=subprocess.PIPE) as test_app:
                for line in test_app.stdout:
                    test_out = line
                test_out_list = test_out.decode().split(' | ')
                self.assertTrue(len(test_out_list) == 5 and \
                                test_out_list[0] == 'DEBUG' and \
                                test_out_list[1] == 'http_logger' and \
                                test_out_list[2].split(' ')[0] == str(datetime.datetime.now().date()) and \
                                test_out_list[3] == '10' and \
                                test_out_list[4][:-1] == 'Starting the app')

                test_app.kill()
            server.kill()
        test_log_file = str(Path(os.getcwd()).parents[0]) + '/my_app.log'
        with open(test_log_file, 'r') as log_file:
            test_log = log_file.readlines()[-1]
            test_log_list = test_log.split(' | ')
            self.assertTrue(len(test_log_list) == 6 and \
                            test_log_list[0] == 'server_logger' and \
                            test_log_list[1] == 'DEBUG' and \
                            test_log_list[2] == 'http_logger' and \
                            test_log_list[3].split(' ')[0] == str(datetime.datetime.now().date()) and \
                            test_log_list[4] == '10' and \
                            test_log_list[5][:-1] == 'Starting the app')
