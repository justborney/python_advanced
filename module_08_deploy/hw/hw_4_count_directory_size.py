"""
В своей работе программист должен часто уметь решать рутинные задачи.

Хорошим примером такой задачи является вычисление суммарного размера директории.

Пожалуйста реализуйте функцию, которая на вход принимает путь до папки
    в виде стрки или объекта Path
и возвращает суммарный объём директории в байтах.

В случае, если на вход функции передаётся несуществующий путь или НЕ директория,
    функция должна выкинуть исключение ValueError с красивым описание ошибки
"""
import os
from pathlib import Path
from typing import Union

size = 0


def calculate_directory_size(directory_path: Union[str, Path] = ".") -> int:
    global size

    if isinstance(directory_path, str) or isinstance(directory_path, Path):
        address = os.path.abspath(directory_path)
    else:
        raise ValueError('Неверный ввод директории')

    if os.path.exists(address):
        for elem in os.listdir(address):
            if os.path.isdir(os.path.join(address, elem)):
                calculate_directory_size(os.path.join(address, elem))
            else:
                size += os.path.getsize(os.path.join(address, elem))
    else:
        raise ValueError('Неверный ввод директории')

    return size
