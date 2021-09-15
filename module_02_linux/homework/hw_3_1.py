"""
Напишите  flask endpoint, который показывал бы превью файла.
Он должен принимать на вход 2 параметра - SIZE (integer) и RELATIVE_PATH -
и выводить первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен будет вернуть 2 строки.
В первой строке будет содержаться полезная информация о файле (его абсолютный путь и размер файла в символах).
После переноса строки будет приведено первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path -- написанный жирным абсолютный путь до файла
result_size -- длина result_text в символах
result_text -- первые SIZE символов файла . Если размер файла больше SIZE, верните только первые SIZE символов

Перенос строки нужно осуществить с помощью html тэга <br>

PS в python абсолютный путь до файла можно узнать вот так
>>> import os
>>> print(os.path.abspath('<some_file_name>'))

"""
import os

from flask import Flask

app = Flask(__name__)


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str) -> str:
    """
    Func returns info and preview of the given file
    :param size:
    :param relative_path: str
    :return: str <abs_path> <result_size><br> <result_text>
    """
    file_path = relative_path.split('/')[-1]
    abs_path = os.path.abspath(file_path)
    with open(abs_path, 'r', encoding='utf8') as test_file:
        result_text = test_file.read(size)
    if len(result_text) < size:
        result_size = len(result_text)
    else:
        result_size = size
    return f'Абсолютный путь до файла: <b>{abs_path}</b>. Количество символов: {result_size}<br> ' \
           f'Превью файла: {result_text}'


if __name__ == "__main__":
    app.run(debug=True)
