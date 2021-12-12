import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_2_database.db") as connect:
        cursor = connect.cursor()
        # 01
        cursor.execute("SELECT * FROM 'salaries' WHERE `salary` < 5000")
        # 02
        total_salary = 0
        cursor.execute("SELECT salary FROM 'salaries'")
        result = cursor.fetchall()
        for salary in result:
            total_salary += salary[0]
        average_salary = round(total_salary / len(result), 3)
        print(f'Средняя зарплата {average_salary}')
        # 03
        cursor.execute("SELECT salary FROM 'salaries'")
        result = sorted(cursor.fetchall())
        mediana_salary = (result[int(len(result) / 2 - 1)][0] + result[int(len(result) / 2)][0]) / 2
        print(f'Медианная зарплата {mediana_salary}')
        # 04
        T = 0
        K = 0
        cursor.execute("SELECT salary FROM 'salaries'")
        result = sorted(cursor.fetchall())
        ten_percent_quantity = int(len(result) * 0.1)
        for salary in result[:-ten_percent_quantity]:
            K += salary[0]
        for salary in result[-ten_percent_quantity:]:
            T += salary[0]
        F = round(T / K, 3)
        print(f'Число социального неравенства {F}')
