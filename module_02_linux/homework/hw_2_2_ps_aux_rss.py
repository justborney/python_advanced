"""
С помощью команды ps можно посмотреть список процессов, запущенных текущим пользователем.
Особенно эта команда выразительна с флагами
    $ ps aux
Запустите эту команду, output сохраните в файл, например вот так
$ ps aux > output_file.txt
В этом файле вы найдёте информацию обо всех процессах, запущенных в системе.
В частности там есть информация о потребляемой процессами памяти - это столбец RSS .
Напишите в функцию python, которая будет на вход принимать путь до файла с output
и на выход возвращать суммарный объём потребляемой памяти в человеко-читаемом формате.
Это означает, что ответ надо будет перевести в байты, килобайты, мегабайты и тд.

Для перевода можете воспользоваться функцией _sizeof_fmt
"""


def _sizeof_fmt(num, suffix="B"):
    for unit in ["", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def get_summary_rss(ps_output_file_path: str) -> str:
    """
    Func returns total volume of used memory that reading from file
    :param ps_output_file_path: path to ps aux result file
    :return: str with total volume of used memory
    """
    with open(ps_output_file_path, 'r', encoding='utf8') as ps_data:
        ps_data_line = ps_data.readlines()
        rss_column_number = 5
        rss_sum = 0
        for column in ps_data_line:
            try:
                rss_sum += int(column.split()[rss_column_number])
            except ValueError:
                continue
    return f'Total volume of used memory is {_sizeof_fmt(rss_sum)}'


if __name__ == "__main__":
    print(get_summary_rss("ps_aux_output.txt"))
