from typing import Union, Callable
from operator import sub, mul, div, add


OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        print("wrong operator type", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        print("wrong operator value", value)
        raise ValueError("wrong operator value")

    return OPERATORS[value]
