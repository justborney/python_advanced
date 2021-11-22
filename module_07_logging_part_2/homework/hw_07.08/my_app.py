import logging.config

from log_conf import dict_config

logging.config.dictConfig(dict_config)
app_logger = logging.getLogger("http_logger")


def my_app_for_http_handler():
    app_logger.debug("Starting the app")
    app_logger.info("App is working")
    app_logger.debug("Stop the app")


if __name__ == "__main__":
    my_app_for_http_handler()
