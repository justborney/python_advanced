import datetime
import typing as tp

import requests

import logging

# logging.basicConfig(level=logging.DEBUG)
from werkzeug.serving import WSGIRequestHandler

WSGIRequestHandler.protocol_version = "HTTP/1.1"


class BookClient:
    BOOK_URL = 'http://127.0.0.1:5000/api/books'
    AUTHOR_URL = 'http://127.0.0.1:5000/api/authors'
    HEADERS = {'content-type': 'application/json', 'Accept-Encoding': 'application/json'}
    TIMEOUT = 5

    def __init__(self):
        self._session = requests.Session()

    def get_all_books(self) -> tp.Dict:
        response = self._session.get(self.BOOK_URL, timeout=self.TIMEOUT)
        return response.json()

    def get_book_by_id(self, book_id: int) -> tp.Dict:
        response = self._session.get(self.BOOK_URL + f'/{book_id}', timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: tp.Dict) -> tp.Dict:
        response = self._session.post(self.BOOK_URL, json=data, headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def change_book(self, data: tp.Dict, book_id: int) -> tp.Dict:
        response = self._session.put(self.BOOK_URL + f'/{book_id}',
                                     json=data, headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def delete_book(self, book_id: int) -> str:
        response = self._session.delete(self.BOOK_URL + f'/{book_id}', timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.text
        else:
            raise ValueError('Wrong book id. Response message: {}'.format(response.json()))

    def get_all_authors(self) -> tp.Dict:
        response = self._session.get(self.AUTHOR_URL, timeout=self.TIMEOUT)
        return response.json()

    def get_all_authors_books_by_id(self, author_id: int) -> tp.Dict:
        response = self._session.get(self.AUTHOR_URL + f'/{author_id}', headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong author id. Response message: {}'.format(response.json()))

    def add_new_author(self, data: tp.Dict) -> tp.Dict:
        response = self._session.post(self.AUTHOR_URL, json=data, headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def change_author(self, data: tp.Dict, author_id: int) -> tp.Dict:
        response = self._session.put(self.AUTHOR_URL + f'/{author_id}',
                                     json=data, headers=self.HEADERS, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def delete_author(self, author_id: int) -> str:
        response = self._session.delete(self.AUTHOR_URL + f'/{author_id}', timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.text
        else:
            raise ValueError('Wrong author id. Response message: {}'.format(response.json()))


if __name__ == '__main__':
    c = BookClient()

    # requests_count_list = [10, 50, 100]
    #
    # for requests_count in requests_count_list:
    #     print(f'Start lap for {requests_count} requests')
    #     start_time = datetime.datetime.now()
    #     i = 0
    #     while i < requests_count / 5:
    #         c.get_all_books()
    #         c.get_book_by_id(1)
    #         c.get_all_authors()
    #         c.get_all_authors_books_by_id(3)
    #         c.get_all_books()
    #         i += 1
    #     finish_time = datetime.datetime.now()
    #     delta_time = finish_time - start_time
    #     print(delta_time)
