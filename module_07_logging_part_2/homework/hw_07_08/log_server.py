import logging.config

from flask import Flask, request
from module_07_logging_part_2.homework.hw_07_08.log_server_conf import dict_config

app = Flask(__name__)

logging.config.dictConfig(dict_config)
server_logger = logging.getLogger("server_logger")


@app.route('/logger', methods=["POST"])
def log_server_func():
    try:
        server_logger.info(request.form['levelname'] + " | " +
                           request.form['name'] + " | " +
                           request.form['asctime'] + " | " +
                           request.form['lineno'] + " | " +
                           request.form['message'])
        return "OK", 200
    except Exception:
        return 'Bad request', 400


if __name__ == '__main__':
    app.run(debug=False, port=5555)
