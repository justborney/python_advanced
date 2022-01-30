import sqlite3
from typing import List

DATA = [
    {'title': 'A Byte of Python', 'author': 'Swaroop C. H.', 'views': 0},
    {'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville', 'views': 0},
    {'title': 'War and Peace', 'author': 'Leo Tolstoy', 'views': 0},
]


class Book:

    def __init__(self, title: str, author: str, id: int = 0, views: int = 0):
        self.id = id
        self.title = title
        self.author = author
        self.views = views

    def __getitem__(self, item):
        return getattr(self, item)


def init_db(initial_records: List[dict]):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='table_books';"
        )
        exists = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                'CREATE TABLE `table_books`'
                '(id INTEGER PRIMARY KEY AUTOINCREMENT, title, author, views)'
            )
            cursor.executemany(
                'INSERT INTO `table_books` '
                '(title, author, views) VALUES (?, ?, ?)',
                [(item['title'], item['author'], item['views']) for item in initial_records]
            )


def books_count():
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT (*) from `table_books`')
        total_count, *_ = cursor.fetchone()
        return total_count


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from `table_books`')
        all_books = cursor.fetchall()
        for book in all_books:
            cursor.execute(increase_book_views(), (book[3] + 1, book[0]))
        return [Book(*row) for row in all_books]


def add_book_func(form) -> tuple:
    new_book = Book(form.data['title'], form.data['author'])
    added = False
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT (*) from `table_books` '
                       'WHERE title = ? and author = ?',
                       (form.data['title'], form.data['author']))
        count, *_ = cursor.fetchone()
        if count == 0:
            cursor.execute(
                'INSERT INTO `table_books` '
                '(title, author, views) VALUES (?, ?, ?)',
                (form.data['title'], form.data['author'], new_book.views)
            )
            added = True
    return new_book, added


def searching_books_by_author(form) -> tuple:
    author = form.data['author']
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from `table_books` '
                       'WHERE author = ?',
                       (author,))
        result = cursor.fetchall()
        for book in result:
            cursor.execute(increase_book_views(), (book[3] + 1, book[0]))
    return author, result


def increase_book_views() -> str:
    sql_update_book_views = """
    UPDATE 'table_books'
    SET views = ?
    WHERE id = ?
    """
    return sql_update_book_views
