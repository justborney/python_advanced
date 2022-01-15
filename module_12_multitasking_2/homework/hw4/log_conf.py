import logging


class CustomFileHandler(logging.Handler):

    def __init__(self, file_name, mode='a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)

        with open(self.file_name, mode=self.mode) as log_file:
            log_file.write(message + '\n')


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "base"
        },
        "file": {
            "()": CustomFileHandler,
            "level": "INFO",
            "formatter": "base",
            "file_name": "lof_file.txt",
            "mode": "a"
        }
    },
    "loggers": {
        "custom_logger": {
            "level": "INFO",
            "handlers": ["file", "console"],
        }
    },
}
