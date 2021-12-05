import logging.config

from utils import string_to_operator
from logger_setup import dict_config
# from OOP_logger_setup import app_log

logging.config.dictConfig(dict_config)
app_logger = logging.getLogger("hw_07.01.app")

# app_logger = app_log()


def calc(args):
    app_logger.debug(f"Arguments: {args}")
    # print("Arguments: ", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        app_logger.exception("Error while converting number 1")
        # print("Error while converting number 1")
        # print(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        app_logger.exception("Error while converting number 2")
        # print("Error while converting number 1")
        # print(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    app_logger.info(f"Result: {result}")
    # print(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    calc([1, 4, '+'])
