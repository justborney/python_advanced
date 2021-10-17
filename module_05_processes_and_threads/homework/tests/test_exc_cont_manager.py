from module_05_processes_and_threads.homework.hw_02_02 import exc_cont_manager
import unittest


class TestExcListManager(unittest.TestCase):
    def test_can_not_handle_exc_not_in_list(self):
        result = exc_cont_manager(exceptions=('Attribute', 'Error'))
        self.assertEqual("'_io.TextIOWrapper' object has no attribute 'undefined'", result)

    def test_can_ignore_exc_in_list(self):
        result = exc_cont_manager(exceptions=(FileNotFoundError, AttributeError))
        self.assertEqual(None, result)
