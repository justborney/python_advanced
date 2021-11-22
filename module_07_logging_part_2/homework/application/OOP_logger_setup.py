import logging


class CustomHandler(logging.Handler):
    def __init__(self, file_name, mode='a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        with open(self.file_name + record.levelname + '.log', mode=self.mode) as file:
            file.write(message + '\n')


formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s")
handler = logging.StreamHandler()
file_handler = CustomHandler('', 'a')

handler.setFormatter(formatter)
file_handler.setFormatter(formatter)


def app_log():
    app_logger = logging.getLogger("hw_07.01.app")
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(handler)
    app_logger.addHandler(file_handler)

    return app_logger


def utils_log():
    utils_logger = logging.getLogger("hw_07.01.app.utils")
    utils_logger.setLevel(logging.DEBUG)
    utils_logger.propagate = False
    utils_logger.addHandler(handler)
    utils_logger.addHandler(file_handler)

    return utils_logger
