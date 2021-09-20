import datetime
import unittest

from ..person import Person


class TestDecrypt(unittest.TestCase):
    def test_can_get_age(self):
        my_person = Person('Anton', 2000, 'SPb, Nevskiy av., 1')
        expected_res = datetime.datetime.now().year - 2000
        function_res = my_person.get_age()
        self.assertEqual(expected_res, function_res)

    def test_can_get_name(self):
        my_person = Person('Anton', 2000, 'SPb, Nevskiy av., 1')
        expected_res = 'Anton'
        function_res = my_person.get_name()
        self.assertEqual(expected_res, function_res)

    def test_can_get_address(self):
        my_person = Person('Anton', 2000, 'SPb, Nevskiy av., 1')
        expected_res = 'SPb, Nevskiy av., 1'
        function_res = my_person.get_address()
        self.assertEqual(expected_res, function_res)

    def test_is_not_homeless(self):
        my_person = Person('Anton', 2000, 'SPb, Nevskiy av., 1')
        expected_res = False
        function_res = my_person.is_homeless()
        self.assertEqual(expected_res, function_res)

    def test_is_homeless(self):
        my_person = Person('Anton', 2000, None)
        expected_res = True
        function_res = my_person.is_homeless()
        self.assertEqual(expected_res, function_res)

    def test_can_set_name(self):
        my_person = Person('Anton', 2000, 'SPb, Nevskiy av., 1')
        expected_res = 'Andrey'
        my_person.set_name('Andrey')
        function_res = my_person.get_name()
        self.assertEqual(expected_res, function_res)

    def test_can_set_address(self):
        my_person = Person('Anton', 2000, 'SPb, Nevskiy av., 1')
        expected_res = 'Ufa, Lenina st., 2'
        my_person.set_address('Ufa, Lenina st., 2')
        function_res = my_person.get_address()
        self.assertEqual(expected_res, function_res)

    def test_can_not_set_wrong_age(self):
        with self.assertRaises(ValueError):
            Person('Anton', 2500, 'SPb, Nevskiy av., 1')
