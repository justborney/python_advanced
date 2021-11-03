import logging
import os
import string

logger = logging.getLogger(__name__)


def func1():
    logger.info("Шаг 1")
    logger.debug("Это просто разминка")

    while True:
        data = input("Ваш ответ? ")

        try:
            number = int(data)

            if number != 9973:
                logger.debug("Нам нужно максимальное простое число меньшее чем 10000")
                print("Не правильно!")
            break
        except Exception:
            pass

    print("Шаг 1 пройден")


def func2():
    logger.info("Шаг 2")

    logger.debug("Задайте переменной окружения SKILLBOX значение awesome")
    logger.debug("Вы можете задать значение переменной окружения вот так:")
    logger.debug("$ export VARNAME=value")

    while True:
        input("Для продолжения нажмите ENTER...")

        try:
            if os.environ["SKILLBOX"].lower() == "awesome":
                break
        except Exception:
            pass

        print("Вы не готовы...")

    print("Шаг 2 пройден")


def func3():
    logger.info("Шаг 3")

    logger.debug("Создайте файл hw7.txt с английским палиндромом внутри")
    while True:
        try:
            input("Для продолжения нажмите ENTER...")

            with open("hw7.txt", "r") as fi:
                data = fi.read().lower()

                data_str = [it for it in data if it in string.ascii_lowercase]

                if data_str == data_str[::-1]:
                    break

                logger.debug(f"{data_str} != {data_str[::-1]}")
        except Exception:
            pass

        print("Не работает...")

    print("Шаг 3 пройден")


def what_went_wrong():
    func1()
    func2()
    func3()


if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")
    what_went_wrong()
