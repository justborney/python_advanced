import unittest

from ..hw_1_2 import app


class TestRegistration(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def form(self, email, phone, name, address, index):
        return self.app.post(self.base_url, data=dict(
            email=email,
            phone=phone,
            name=name,
            address=address,
            index=index
        ))

    def test_can_post_with_valid_data(self):
        response = self.form(email="qwerty@mail.ru",
                             phone=1234567899,
                             name="Ivan",
                             address="qwerty, 123456789",
                             index=500)
        self.assertEqual(b'Successfully registered user qwerty@mail.ru with phone +71234567899', response.data)
        self.assertEqual(200, response.status_code)

    def test_can_not_post_without_email(self):
        response = self.form(email="",
                             phone=1234567899,
                             name="Ivan",
                             address="qwerty, 123456789",
                             index=500)
        self.assertEqual(b"Invalid input, {'email': ['This field is required.']}", response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_wrong_email(self):
        response = self.form(email="qwertymail.ru",
                             phone=1234567899,
                             name="Ivan",
                             address="qwerty, 123456789",
                             index=500)
        print(response.data)
        self.assertEqual(b"Invalid input, {'email': ['Invalid email address.']}", response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_without_phone(self):
        response = self.form(email="qwerty@mail.ru",
                             phone=None,
                             name="Ivan",
                             address="qwerty, 123456789",
                             index=500)
        self.assertEqual(b"Invalid input, {'phone': ['This field is required.']}", response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_wrong_phone(self):
        response = self.form(email="qwerty@mail.ru",
                             phone=12345678999,
                             name="Ivan",
                             address="qwerty, 123456789",
                             index=500)
        self.assertEqual(b"Invalid input, {'phone': ['Number must be between 1000000000 and 9999999999.']}",
                         response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_phone_with_letters(self):
        response = self.form(email="qwerty@mail.ru",
                             phone="asd",
                             name="Ivan",
                             address="qwerty, 123456789",
                             index=500)
        self.assertEqual(
            b"Invalid input, {'phone': ['Not a valid integer value', "
            b"'Number must be between 1000000000 and 9999999999.']}", response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_without_name(self):
        response = self.form(email="qwerty@mail.ru",
                             phone=1234567899,
                             name=None,
                             address="qwerty, 123456789",
                             index=500)
        self.assertEqual(b"Invalid input, {'name': ['This field is required.']}", response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_without_address(self):
        response = self.form(email="qwerty@mail.ru",
                             phone=1234567899,
                             name="Ivan",
                             address=None,
                             index=500)
        self.assertEqual(b"Invalid input, {'address': ['This field is required.']}", response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_without_index(self):
        response = self.form(email="qwerty@mail.ru",
                             phone=1234567899,
                             name="Ivan",
                             address="qwerty, 123456789",
                             index=None)
        self.assertEqual(b"Invalid input, {'index': ['This field is required.']}", response.data)
        self.assertEqual(400, response.status_code)

    def test_can_not_post_index_with_letters(self):
        response = self.form(email="qwerty@mail.ru",
                             phone=1234567899,
                             name="Ivan",
                             address="qwerty, 123456789",
                             index="asd")
        self.assertEqual(b"Invalid input, {'index': ['Not a valid integer value']}", response.data)
        self.assertEqual(400, response.status_code)
