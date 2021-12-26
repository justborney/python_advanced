import requests
import sqlite3

PAGE_COUNT = 1
QUANTITY = 19
PERSONS = []


def record_data():
    connection = sqlite3.connect('hw2.db')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS people "
                   "(Name TEXT, Gender TEXT)")
    cursor.executemany("INSERT INTO people VALUES (?, ?)", PERSONS)
    connection.commit()
    connection.close()


def star_wars_api():
    global PAGE_COUNT
    global QUANTITY
    global PERSONS
    count = QUANTITY - (PAGE_COUNT - 1) * 10
    people = requests.get(f'https://swapi.dev/api/people/?page={PAGE_COUNT}').json()
    if count >= 0:
        try:
            for i in range(count):
                PERSONS.append((people['results'][i]['name'], people['results'][i]['gender']))
        except IndexError:
            if QUANTITY >= people['count']:
                print('Incorrect request')
                exit()
            else:
                PAGE_COUNT += 1
                star_wars_api()


if __name__ == "__main__":
    star_wars_api()
    record_data()
