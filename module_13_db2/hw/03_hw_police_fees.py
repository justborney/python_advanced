"""
Вы работаете программистом в IT отделе ГИБДД.
    Ваш отдел отвечает за обслуживание камер,
    которые фиксируют превышения скорости и выписывают автоматические штрафы.
За последний месяц к вам пришло больше тысячи жалоб на ошибочно назначенные штрафы,
    из которых около 100 были признаны и правда ошибочными.

Список из дат и номеров автомобилей ошибочных штрафов прилагается к заданию,
    пожалуйста удалите записи об этих штрафах из таблицы `table_fees`
"""
import sqlite3

sql_del_req = """
DELETE FROM `table_fees`
WHERE truck_number = ? 
AND timestamp = ?;
"""


def delete_wrong_fees(c: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file, 'r') as records_file:
        records_file.readline()
        while records_file:
            record = records_file.readline()[:-1]

            if not record:
                break

            record_data = record.split(',')
            car_number = record_data[0]
            timestamp = record_data[1]
            c.execute(sql_del_req, (car_number, timestamp))


if __name__ == "__main__":
    with sqlite3.connect("hw.db") as conn:
        cursor = conn.cursor()

        delete_wrong_fees(cursor, "wrong_fees.csv")
