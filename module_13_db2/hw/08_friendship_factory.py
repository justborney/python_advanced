"""
На заводе "Дружба" работает очень дружный коллектив.
Рабочие работают посменно, в смене -- 10 человек.
На смену заходит 366 .

Бухгалтер завода составила расписание смен и занесла его в базу данных
    в таблицу `table_work_schedule`, но совершенно не учла тот факт,
    что все сотрудники люди спортивные и ходят на различные спортивные кружки:
        1. футбол (проходит по понедельникам)
        2. хоккей (по вторникам
        3. шахматы (среды)
        4. SUP сёрфинг (четверг)
        5. бокс (пятница)
        6. Dota2 (суббота)
        7. шах-бокс (воскресенье)

Как вы видите, тренировки по этим видам спорта проходят в определённый день недели.

Пожалуйста помогите изменить расписание смен с учётом личных предпочтений коллектива
    (или докажите, что то, чего они хотят - не возможно).
"""
import sqlite3

import dateutil.parser

sql_get_count_football = """
SELECT COUNT (*) FROM 'table_friendship_employees'
WHERE preferable_sport = ?
"""


def update_work_schedule(c: sqlite3.Cursor) -> None:
    count = []

    c.execute(sql_get_count_football, ('футбол',))
    football, *_ = c.fetchone()
    count.append(football)
    print('football -', football)

    c.execute(sql_get_count_football, ('хоккей',))
    hockey, *_ = c.fetchone()
    count.append(hockey)
    print('hockey -', hockey)

    c.execute(sql_get_count_football, ('шахматы',))
    chess, *_ = c.fetchone()
    count.append(chess)
    print('chess -', chess)

    c.execute(sql_get_count_football, ('SUP сёрфинг',))
    SUP, *_ = c.fetchone()
    count.append(SUP)
    print('SUP -', SUP)

    c.execute(sql_get_count_football, ('бокс',))
    box, *_ = c.fetchone()
    count.append(box)
    print('box -', box)

    c.execute(sql_get_count_football, ('Dota2',))
    dota2, *_ = c.fetchone()
    count.append(dota2)
    print('dota2 -', dota2)

    c.execute(sql_get_count_football, ('шах-бокс',))
    check_box, *_ = c.fetchone()
    count.append(check_box)
    print('check_box -', check_box)

    print('')

    c.execute("""
    SELECT * FROM 'table_friendship_schedule'
    WHERE date = '2020-01-01'
    """)

    record = c.fetchall()[0]
    date = dateutil.parser.parse(record[1])
    week_day = date.date().weekday()
    print('2020-01-01 week_day -', week_day)

    print('')

    print('понедельник - 52')
    print('вторник - 52')
    print('среда - 53')
    print('четверг - 53')
    print('пятница - 52')
    print('суббота - 52')
    print('воскресенье - 52')

    print('')

    print('Невозможно равномерно распределить')


if __name__ == '__main__':
    with sqlite3.connect("hw.db") as conn:
        cursor = conn.cursor()

        update_work_schedule(cursor)
