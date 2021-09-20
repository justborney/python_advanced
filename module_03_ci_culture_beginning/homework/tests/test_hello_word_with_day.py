import datetime
import unittest

from module_03_ci_culture_beginning.materials.previous_hw_test.hello_word_with_day import app


class TestHelloWorldApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    def test_can_get_correct_username_with_weekday(self):
        day_to_word_map = {
            0: "Хорошего понедельника",
            1: "Хорошего вторника",
            2: "Хорошей среды",
            3: "Хорошего четверга",
            4: "Хорошей пятницы",
            5: "Хорошей суббота",
            6: "Хорошего воскресенья"
        }
        day_num = 0
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()

        for key, value in day_to_word_map.items():
            if value == response_text.split('. ')[1][:-1]:
                day_num = key

        self.assertTrue(day_num == datetime.datetime.today().weekday())
