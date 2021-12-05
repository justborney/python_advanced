import logging.handlers
import sys


class CustomRotatingHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when, interval, backupCount, encoding, delay, utc, atTime):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)


class CustomHandler(logging.Handler):
    def __init__(self, file_name, mode):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        # with open(self.file_name + record.levelname + '.log', mode=self.mode) as file:
        with open(self.file_name, mode=self.mode) as file:
            file.write(message + '\n')


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
        }
    },
    "handlers": {
        "screen": {
            "class": "logging.StreamHandler",
            "level": logging.DEBUG,
            "formatter": "simple",
            "stream": sys.stdout
        },
        "file": {
            "()": CustomHandler,
            "level": logging.DEBUG,
            "formatter": "simple",
            "file_name": "my_app.log",
            "mode": "a"
        },
        "rotate": {
            "()": CustomRotatingHandler,
            "level": logging.DEBUG,
            "formatter": "simple",
            "filename": "my_app.log",
            "when": "h",
            "interval": 10,
            "backupCount": 0,
            "encoding": None,
            "delay": False,
            "utc": False,
            "atTime": None
        }
    },
    "loggers": {
        "hw_07.01.app": {
            "level": "NOTSET",
            "handlers": ["screen", "file"],
        },
        "hw_07.01.utils": {
            "level": "INFO",
            # "handlers": ["screen", "file", "rotate"],
            "handlers": ["screen", "rotate"],
        }
    },
}
