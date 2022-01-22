"""
Иван Совин - эффективный менеджер.
Когда к нему приходит сотрудник просить повышение з/п -
    Иван может повысить её только на 10%.

Если после повышения з/п сотрудника будет больше з/п самого
    Ивана Совина - сотрудника увольняют, в противном случае з/п
    сотрудника повышают.

Давайте поможем Ивану стать ещё эффективнее,
    автоматизировав его нелёгкий труд.
    Пожалуйста реализуйте функцию которая по имени сотрудника
    либо повышает ему з/п, либо увольняет сотрудника
    (удаляет запись о нём из БД).

Таблица с данными называется `table_effective_manager`
"""
import sqlite3

sql_get_worker = """
SELECT * FROM 'table_effective_manager'
WHERE name = ?
"""

sql_delete_worker = """
DELETE FROM 'table_effective_manager'
WHERE name = ?
"""

sql_update_worker_salary = """
UPDATE 'table_effective_manager'
SET salary = ?
WHERE name = ?
"""


def ivan_sovin_the_most_effective(
        c: sqlite3.Cursor,
        name: str,
) -> None:
    c.execute(sql_get_worker, ('Иван Совин',))
    ivan_payment = c.fetchone()[2]

    c.execute(sql_get_worker, (name,))
    worker_payment = c.fetchone()[2]
    worker_new_payment = round(1.1 * worker_payment, 3)

    if worker_new_payment > ivan_payment:
        c.execute(sql_delete_worker, (name,))
    c.execute(sql_update_worker_salary, (worker_new_payment, name))


if __name__ == "__main__":
    with sqlite3.connect("hw.db") as conn:
        cursor = conn.cursor()

        ivan_sovin_the_most_effective(cursor, 'Семёнова Ж.Ц.')
