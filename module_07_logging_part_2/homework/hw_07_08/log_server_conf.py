import logging.handlers


class CustomHandler(logging.Handler):
    def __init__(self, file_name, mode='a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        with open(self.file_name, mode=self.mode) as file:
            file.write(message + '\n')


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(name)s | %(message)s"
        }
    },
    "handlers": {
        "file": {
            "()": CustomHandler,
            "level": logging.DEBUG,
            "formatter": "simple",
            "file_name": "my_app.log",
            "mode": "a"
        },
    },
    "loggers": {
        "server_logger": {
            "level": "DEBUG",
            "handlers": ["file"],
        }
    },
}
