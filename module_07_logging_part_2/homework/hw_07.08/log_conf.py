import logging.handlers
import sys


class CustomHTTPHandler(logging.handlers.HTTPHandler):
    def __init__(self, host: str, url: str):
        super().__init__(host, url,
                         method='POST',
                         secure=False,
                         credentials=None,
                         context=None)


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
            "()": CustomHTTPHandler,
            "level": logging.DEBUG,
            "host": "localhost:5555",
            "url": "/logger"
        }
    },
    "loggers": {
        "http_logger": {
            "level": "DEBUG",
            "handlers": ["screen", "file"],
        }
    },
}
