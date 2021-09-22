import unittest

from ..decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    def test_one_point_rule(self):
        input_str = 'абра-кадабра.'
        expected_res = 'абра-кадабра'
        function_res = decrypt(input_str)
        self.assertEqual(expected_res, function_res)

    def test_two_points_rule(self):
        input_str = 'абраа..-кадабра'
        expected_res = 'абра-кадабра'
        function_res = decrypt(input_str)
        self.assertEqual(expected_res, function_res)

    def test_two_points_then_one_point_rules(self):
        input_str = 'абрау...-кадабра'
        expected_res = 'абра-кадабра'
        function_res = decrypt(input_str)
        self.assertEqual(expected_res, function_res)

    def test_blank_line_result(self):
        input_str = 'абра........'
        expected_res = ''
        function_res = decrypt(input_str)
        self.assertEqual(expected_res, function_res)

    def test_can_not_proceed_int_input(self):
        input_str = 123
        with self.assertRaises(TypeError):
            decrypt(input_str)
