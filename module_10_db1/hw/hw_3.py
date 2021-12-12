import sqlite3

with sqlite3.connect("hw_3_database.db") as connect:
    cursor = connect.cursor()
    # 01
    table_list = ['table_1', 'table_2', 'table_3']
    for table in table_list:
        cursor.execute(f"SELECT * FROM {table}")
        result = len(cursor.fetchall())
        print(f'Записей в "{table}" {result}')
    # 02
    cursor.execute("SELECT DISTINCT value FROM 'table_1'")
    result = len(cursor.fetchall())
    print(f'Количество уникальных значений в "table_1" {result}')
    # 03
    cursor.execute("SELECT value FROM 'table_1' INTERSECT "
                   "SELECT value FROM 'table_2' ")
    table_1_and_2_intersect_quantity = len(cursor.fetchall())
    print(f'Количество записей из "table_1", присутствующих в "table_2" {table_1_and_2_intersect_quantity}')
    # 04
    cursor.execute("SELECT value FROM 'table_1' INTERSECT "
                   "SELECT value FROM 'table_2' INTERSECT "
                   "SELECT value FROM 'table_3'")
    table_1_2_3_intersect_quantity = len(cursor.fetchall())
    print(f'Количество записей из "table_1", присутствующих в "table_2" и в "table_3" {table_1_2_3_intersect_quantity}')
