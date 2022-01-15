from multiprocessing import Pool

import requests
import sqlite3

QUANTITY = 19


class StarWarsAPIParser:
    def __init__(self, page, count, persons=None):
        if persons is None:
            persons = []
        self.page = page
        self.count = count
        self.persons = persons

        self.run()

    def run(self):
        people = requests.get(f'https://swapi.dev/api/people/?page={self.page}').json()

        for i in range(self.count):
            self.persons.append((people['results'][i]['name'], people['results'][i]['gender']))
        self.record_data()

    def record_data(self):
        connection = sqlite3.connect('hw1.db')
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

    pool = Pool(processes=parsers_count)

    for i in range(1, parsers_count):
        pool.apply_async(StarWarsAPIParser(i, 10))
    pool.apply_async(StarWarsAPIParser(parsers_count, last_parser_length))

    pool.close()
    pool.join()


if __name__ == "__main__":
    star_wars_api()
