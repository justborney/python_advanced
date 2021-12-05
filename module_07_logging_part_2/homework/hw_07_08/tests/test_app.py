import logging.config

from module_07_logging_part_2.homework.hw_07_08.log_conf import dict_config

logging.config.dictConfig(dict_config)
app_logger = logging.getLogger("http_logger")


def my_app_for_http_handler():
    app_logger.debug("Starting the app")


if __name__ == "__main__":
    my_app_for_http_handler()
