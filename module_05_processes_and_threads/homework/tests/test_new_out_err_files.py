import os

from module_05_processes_and_threads.homework.hw_03_01 import StdErrOutManager
import unittest


class TestNewErrOutManager(unittest.TestCase):
    def test_can_write_data(self):
        test_data = 'Test data'
        file_path = os.path.abspath('test_file.txt')
        with StdErrOutManager(file_path, 'w', 'new_out.txt', 'new_err.txt', test_data) as file:
            pass
        file_data_path = os.path.abspath('test_file.txt')
        with open(file_data_path, 'r') as test_file:
            result_data = test_file.readline()
        self.assertEqual(test_data, result_data)

    def test_can_write_out(self):
        test_data = 'Test data'
        file_path = os.path.abspath('test_file.txt')
        with StdErrOutManager(file_path, 'w', 'new_out.txt', 'new_err.txt', test_data):
            pass
        file_out_path = os.path.abspath('new_out.txt')
        with open(file_out_path, 'r') as test_file:
            result_data = test_file.readline()
        self.assertEqual('Success record', result_data)

    def test_can_write_errors(self):
        test_data = ''
        file_path = os.path.abspath('test_file.txt')
        with StdErrOutManager(file_path, 'w', 'new_out.txt', 'new_err.txt', test_data):
            pass
        file_err_path = os.path.abspath('new_err.txt')
        self.assertTrue(os.path.getsize(file_err_path))
