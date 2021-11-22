import logging


class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return str(record).isascii()
