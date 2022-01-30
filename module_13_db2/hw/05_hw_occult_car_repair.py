"""
В 20NN году оккультному автосалону "Чёртово колесо" исполняется ровно 13 лет.
    В честь этого они предлагает своим клиентам уникальную акцию:
    если вы обращаетесь в автосалон в пятницу тринадцатое и ваш автомобиль
    чёрного цвета и марки "Лада" или "BMW", то вы можете поменять колёса со скидкой 13%.
Младший менеджер "Чёртова колеса" слил данные клиентов в интернет,
    поэтому мы можем посчитать, как много клиентов автосалона могли воспользоваться
    скидкой (если бы они об этом знали). Давайте сделаем это!

Реализуйте функцию, c именем get_number_of_luckers которая принимает на вход курсор и номер месяца,
    и в ответ возвращает число клиентов, которые могли бы воспользоваться скидкой автосалона.
    Таблица с данными называется `table_occult_car_repair`
"""
import sqlite3
import dateutil.parser

sql_count_luckers = """
SELECT * FROM 'table_occult_car_repair'
WHERE car_colour = ? 
AND (car_type = ? OR car_type = ?)
"""


def get_number_of_luckers(c: sqlite3.Cursor, month_number: int) -> int:
    c.execute(sql_count_luckers, ('чёрный', 'Лада', 'BMW'))
    results = c.fetchall()

    count = 0
    for record in results:
        record_date = dateutil.parser.parse(record[1])
        if record_date.date().month == month_number \
                and record_date.date().day == 13 \
                and record_date.date().weekday() == 4:
            count += 1
    return count


if __name__ == "__main__":
    with sqlite3.connect("hw.db") as conn:
        cursor = conn.cursor()

        print(get_number_of_luckers(cursor, 11))


# _SQL_request = """
# SELECT COUNT(*) FROM 'table_occult_car_repair' WHERE car_colour = ? and (car_type in (?, ?)) and timestamp LIKE ?
# """
#
#
# def get_number_of_luckers(c: sqlite3.Cursor, month: int) -> int:
#     if len(str(month)) < 2:
#         value = '0' + str(month)
#     else:
#         value = str(month)
#     string = f'%-{value}-%'
#
#     c.execute(_SQL_request, ('чёрный', 'BMW', 'Лада', string))
#     result = c.fetchone()
#     return result[0]