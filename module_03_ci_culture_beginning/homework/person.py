import datetime


class Person:
    def __init__(self, name, year_of_birth, address=''):
        self.name = name
        if year_of_birth <= datetime.datetime.now().year:
            self.yob = year_of_birth
        else:
            raise ValueError('Wrong age')
        self.address = address

    def get_age(self):
        now = datetime.datetime.now()
        return now.year - self.yob

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def is_homeless(self):
        '''
        returns True if address is not set, false in other case
        '''
        return self.address is None
