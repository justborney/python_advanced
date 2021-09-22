import unittest

from ..calc_of_spends import app
from ..calc_of_spends import storage


class TestCalcOfSpends(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        storage[2020] = {4: 486, 10: 28, 12: 457}
        storage[2021] = {5: 1862, 11: 1237}
        self.app = app.test_client()
        self.base_url = '/calculate/'

    def test_can_add_correct_spend_and_date_in_storage(self):
        self.app.get('/add/20210825/378')
        self.assertTrue(storage[2021][8] >= 378)

    def test_can_not_add_spend_with_str_date(self):
        with self.assertRaises(ValueError):
            self.app.get('/add/asdfqwer/378')

    def test_can_get_correct_sum_of_month_spends(self):
        response = self.app.get(self.base_url + '2021/05')
        response_text = response.data.decode()
        self.assertTrue(storage[2021][5] == int(response_text.split(' ')[-1]))

    def test_can_get_correct_sum_of_year_spends(self):
        response = self.app.get(self.base_url + '2021')
        response_text = response.data.decode()
        self.assertTrue((storage[2021][5] + storage[2021][11]) == int(response_text.split(' ')[-1]))
