"""
Юный натуралист Петя решил посетить Юнтоловский заказник на рассвете и записать журнал всех птиц,
    которых он увидел в заказнике. Он написал программу, но, в процессе написания,
    так устал, что уснул на клавиатуре, отчего пол-программы стёрлось.

Наш юный натуралист точно помнит, что программа позволяла добавить в БД новую птицу и говорила ему,
    видел ли он такую птицу раньше.

Помогите восстановить исходный код программы ЮНат v0.1 ,
    реализовав функции log_bird (добавление новой птицы в БД) и check_if_such_bird_already_seen
    (проверка что мы уже видели такую птицу)

Пожалуйста помогите ему, реализовав функцию log_bird .
    При реализации не забудьте про параметризацию SQL запроса!
"""

import datetime
import sqlite3

sql_create_table_birds = """
CREATE TABLE IF NOT EXISTS 'table_birds'(
id INTEGER PRIMARY KEY,
bird_name TEXT NOT NULL,
date_time DATA NOT NULL)
"""

sql_add_bird = """
INSERT INTO `table_birds` (bird_name, date_time) 
VALUES (?, ?)
"""

sql_check_bird = """
SELECT COUNT (*) FROM 'table_birds'
WHERE bird_name = ?
"""


def log_bird(
        c: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    c.execute(sql_add_bird, (bird_name, date_time))


def check_if_such_bird_already_seen(c: sqlite3.Cursor, bird_name: str) -> bool:
    c.execute(sql_check_bird, (bird_name,))
    result, *_ = c.fetchone()

    if result > 1:
        return True
    return False


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name = input("Пожалуйста введите имя птицы\n> ")
    count_str = input("Сколько птиц вы увидели?\n> ")
    count = int(count_str)
    right_now = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("hw.db") as connection:
        cursor = connection.cursor()

        cursor.execute(sql_create_table_birds)

        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
