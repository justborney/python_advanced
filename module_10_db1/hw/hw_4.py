import typing


def find_insert_position(array: typing.List[int], value: int) -> int:
    for elem in array:
        if elem < value:
            continue
        if elem >= value:
            return array.index(elem)


if __name__ == '__main__':
    print(find_insert_position([1, 2, 3, 3, 3, 5], 4))
