import sqlite3
from dataclasses import dataclass
from typing import List, Optional, Union, Tuple

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"

BOOK_DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 2},
    {'id': 3, 'title': 'War and Peace', 'author': 3},
]
AUTHOR_DATA = [
    {'id': 0, 'name': 'Swaroop C. H.'},
    {'id': 1, 'name': 'Herman Melville'},
    {'id': 2, 'name': 'Leo Tolstoy'},
]

BOOKS_TABLE_NAME = 'books'
AUTHOR_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author: str
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    name: str
    id: Optional[int] = None

    def __getitem__(self, item) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_books: List[dict], initial_authors: List[dict]) -> None:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master "
            f"WHERE type='table' AND name='{BOOKS_TABLE_NAME}';"
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f'CREATE TABLE `{BOOKS_TABLE_NAME}` '
                f'(id INTEGER PRIMARY KEY AUTOINCREMENT, title, '
                f'author REFERENCES {AUTHOR_TABLE_NAME} (id) ON DELETE CASCADE)'
            )
            cursor.executemany(
                f'INSERT INTO `{BOOKS_TABLE_NAME}` '
                '(title, author) VALUES (?, ?)',
                [(item['title'], item['author']) for item in initial_books]
            )
        cursor.execute(
            "SELECT name FROM sqlite_master "
            f"WHERE type='table' AND name='{AUTHOR_TABLE_NAME}';"
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f'CREATE TABLE {AUTHOR_TABLE_NAME} '
                f'(id INTEGER PRIMARY KEY AUTOINCREMENT, name)'
            )
            for item in initial_authors:
                author_name = item['name']
                cursor.execute(
                    f'INSERT INTO {AUTHOR_TABLE_NAME} (name) VALUES (?)',
                    (author_name,)
                )


def _get_book_obj_from_row(row: Tuple) -> Book:
    return Book(id=row[0], title=row[1], author=row[2])


def _get_author_obj_from_row(row: Tuple) -> Author:
    return Author(id=row[0], name=row[1])


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT `{BOOKS_TABLE_NAME}`.id, `{BOOKS_TABLE_NAME}`.title, `{AUTHOR_TABLE_NAME}`.name '
            f'FROM `{BOOKS_TABLE_NAME}`'
            f'INNER JOIN `{AUTHOR_TABLE_NAME}`'
            f'ON `{BOOKS_TABLE_NAME}`.author = `{AUTHOR_TABLE_NAME}`.id'
        )
        all_books = cursor.fetchall()
    return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    if not get_author_by_name(book.author):
        add_author_by_name(book.author)
    author_id = get_author_by_name(book.author).id
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author) VALUES (?, ?)
            """,
            (book.title, author_id)
        )
        book.id = cursor.lastrowid
    return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT `{BOOKS_TABLE_NAME}`.id, `{BOOKS_TABLE_NAME}`.title, `{AUTHOR_TABLE_NAME}`.name '
            f'FROM `{BOOKS_TABLE_NAME}`'
            f'INNER JOIN `{AUTHOR_TABLE_NAME}`'
            f'ON `{BOOKS_TABLE_NAME}`.author = `{AUTHOR_TABLE_NAME}`.id'
            f'WHERE id = "%s"' % book_id)
        book = cursor.fetchone()
    if book:
        return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    if not get_author_by_name(book.author):
        add_author_by_name(book.author)
    author_id = get_author_by_name(book.author).id
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ? ,
                author = ?
            WHERE id = ?
            """, (book.title, author_id, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """, (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT `{BOOKS_TABLE_NAME}`.id, `{BOOKS_TABLE_NAME}`.title, `{AUTHOR_TABLE_NAME}`.name '
            f'FROM `{BOOKS_TABLE_NAME}`'
            f'INNER JOIN `{AUTHOR_TABLE_NAME}`'
            f'ON `{BOOKS_TABLE_NAME}`.author = `{AUTHOR_TABLE_NAME}`.id'
            f' WHERE title = "%s"' % book_title
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_all_authors() -> List[Author]:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{AUTHOR_TABLE_NAME}`')
        all_authors = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in all_authors]


def get_author_by_name(name: str) -> Optional[Author]:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT * FROM `{AUTHOR_TABLE_NAME}` WHERE name = "%s"' % name
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def add_author_by_name(author: str) -> Author:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHOR_TABLE_NAME}` 
            (name) VALUES (?)
            """,
            (author,)
        )
        new_author = Author(author)
        new_author.id = cursor.lastrowid
        return new_author


def add_author(author: Author) -> Author:
    return add_author_by_name(author.name)


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT * FROM `{AUTHOR_TABLE_NAME}`'
            f'WHERE id = "%s"' % author_id)
        author = cursor.fetchone()
    if author:
        return _get_author_obj_from_row(author)


def get_all_author_books(author_id: int) -> List[Book]:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT `{BOOKS_TABLE_NAME}`.id, `{BOOKS_TABLE_NAME}`.title, `{AUTHOR_TABLE_NAME}`.name '
            f'FROM `{BOOKS_TABLE_NAME}`'
            f'INNER JOIN `{AUTHOR_TABLE_NAME}`'
            f'ON `{BOOKS_TABLE_NAME}`.author = `{AUTHOR_TABLE_NAME}`.id '
            f'WHERE `{AUTHOR_TABLE_NAME}`.id = "%s"' % author_id
        )
        all_books = cursor.fetchall()
    return [_get_book_obj_from_row(row) for row in all_books]


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(ENABLE_FOREIGN_KEY)
        cursor.execute(f"""
        DELETE FROM {AUTHOR_TABLE_NAME}
        WHERE id = ?
        """, (author_id,)
                       )
        conn.commit()


def update_author_by_id(author: Author) -> None:
    with sqlite3.connect('table_books_and_authors.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {AUTHOR_TABLE_NAME}
            SET name = ? 
            WHERE id = ?
            """, (author.name, author.id)
        )
        conn.commit()
