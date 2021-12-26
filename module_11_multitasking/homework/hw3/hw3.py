import threading

import requests
import sqlite3

QUANTITY = 19


class StarWarsAPIParser(threading.Thread):
    def __init__(self, page, count, semaphore: threading.Semaphore, persons=None):
        super().__init__()
        if persons is None:
            persons = []
        self.page = page
        self.count = count
        self.sem = semaphore
        self.persons = persons

    def run(self):
        with self.sem:
            people = requests.get(f'https://swapi.dev/api/people/?page={self.page}').json()

            for i in range(self.count):
                self.persons.append((people['results'][i]['name'], people['results'][i]['gender']))
        self.record_data()

    def record_data(self):
        connection = sqlite3.connect('hw3.db')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS people "
                       "(Name TEXT, Gender TEXT)")
        cursor.executemany("INSERT INTO people VALUES (?, ?)", self.persons)
        connection.commit()
        connection.close()


def star_wars_api():
    global QUANTITY
    parsers_count = 1
    last_parser_length = 10

    if QUANTITY > 10:
        parsers_count = QUANTITY // 10 + 1
        last_parser_length = QUANTITY % 10

    result = requests.get(f'https://swapi.dev/api/people/').json()
    if QUANTITY >= result['count']:
        print('Incorrect request')
        exit()

    semaphore = threading.Semaphore()
    parsers = []
    for i in range(1, parsers_count):
        parser = StarWarsAPIParser(i, 10, semaphore)
        parser.start()
        parsers.append(parser)

    parser = StarWarsAPIParser(parsers_count, last_parser_length, semaphore)
    parser.start()
    parsers.append(parser)

    for parser in parsers:
        parser.join()


if __name__ == "__main__":
    star_wars_api()
