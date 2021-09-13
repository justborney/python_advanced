"""
Напишите функцию, которая будет по output команды ls возвращать средний размер файла в папке.
$ ls -l ./
В качестве аргумента функции должен выступать путь до файла с output команды ls
"""


def get_mean_size(ls_output_path: str) -> float:
    """
    Func returns amount size of files in folders
    :param ls_output_path: path to ls result file
    :return: float amount size of files in folders
    """
    with open(ls_output_path, 'r', encoding='utf8') as ls_data:
        ls_data_line = ls_data.readlines()
        file_size_column_number = 4
        total_files_size = 0
        files_quantity = 0
        for column in ls_data_line:
            try:
                total_files_size += int(column.split()[file_size_column_number])
                files_quantity += 1
            except IndexError:
                continue
    return round(total_files_size / files_quantity, 3)


if __name__ == "__main__":
    print(get_mean_size("ls_output.txt"))
