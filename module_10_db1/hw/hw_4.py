import typing


def find_insert_position(array: typing.List[int], value: int) -> int:
    for elem in array:
        if elem < value:
            continue
        if elem >= value:
            return array.index(elem)


if __name__ == '__main__':
    print(find_insert_position([1, 2, 3, 3, 3, 5], 4))


# ваш способ не очень оптимальный. Все таки бинарный поиск тут поможет. Проверьте замеры скорости:
import random
import time

import numpy


def find_insert_position_2(struct, elem):
    low = 0
    high = len(struct)
    while low < high:
        mid = (low + high) // 2
        if struct[mid] < elem:
            low = mid + 1
        else:
            high = mid

    return low


A = numpy.random.random_integers(1, 10 ** 9, 10 ** 6)
A.sort()

current = time.time()
print('result', find_insert_position_2(A, random.randint(1, 10 ** 8)))
after = time.time()
print('time', after - current)
