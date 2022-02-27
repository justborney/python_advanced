import sqlite3

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"

CREATE_TABLE_DIRECTOR = """
DROP TABLE IF EXISTS 'director';
CREATE TABLE 'director' (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(50) NOT NULL,
    dir_last_name VARCHAR(50) NOT NULL
)
"""

CREATE_TABLE_MOVIE = """
DROP TABLE IF EXISTS 'movie';
CREATE TABLE 'movie' (
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(50) NOT NULL
)
"""

CREATE_TABLE_ACTORS = """
DROP TABLE IF EXISTS 'actors';
CREATE TABLE 'actors' (
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(50) NOT NULL,
    act_last_name VARCHAR(50) NOT NULL,
    act_gender VARCHAR(1) NOT NULL
)
"""

CREATE_TABLE_MOVIE_DIRECTION = """
DROP TABLE IF EXISTS 'movie_direction';
CREATE TABLE 'movie_direction' (
    dir_id INTEGER NOT NULL REFERENCES director(dir_id) ON DELETE CASCADE,
    mov_id INTEGER NOT NULL REFERENCES movie(mov_id) ON DELETE CASCADE
)
"""

CREATE_TABLE_MOVIE_CAST = """
DROP TABLE IF EXISTS 'movie_cast';
CREATE TABLE 'movie_cast' (
    act_id INTEGER NOT NULL REFERENCES actors(act_id) ON DELETE CASCADE,
    mov_id INTEGER NOT NULL REFERENCES movie(mov_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL
)
"""

CREATE_TABLE_OSCAR_AWARDED = """
DROP TABLE IF EXISTS 'oscar_awarded';
CREATE TABLE 'oscar_awarded'(
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER NOT NULL REFERENCES movie(mov_id) ON DELETE CASCADE
)
"""


def create_tables():
    with sqlite3.connect("hw16-1.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLE_DIRECTOR)
        cursor.executescript(CREATE_TABLE_MOVIE)
        cursor.executescript(CREATE_TABLE_ACTORS)
        cursor.executescript(CREATE_TABLE_MOVIE_CAST)
        cursor.executescript(CREATE_TABLE_MOVIE_DIRECTION)
        cursor.executescript(CREATE_TABLE_OSCAR_AWARDED)


if __name__ == '__main__':
    create_tables()
