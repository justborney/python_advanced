import logging.config
from typing import Union, Callable
from operator import sub, mul, truediv, add
from logger_setup import dict_config
# from OOP_logger_setup import utils_log

logging.config.dictConfig(dict_config)
utils_logger = logging.getLogger("hw_07.01.utils")
utils_logger.setLevel(logging.INFO)

# utils_logger = utils_log()

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        utils_logger.critical(f"wrong operator type {value}")
        # print("wrong operator type", value)
        # raise ValueError("wrong operator type")

    if value not in OPERATORS:
        utils_logger.critical(f"wrong operator value {value}")
        # print("wrong operator value", value)
        # raise ValueError("wrong operator value")

    return OPERATORS[value]
