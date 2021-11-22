import logging

from flask import Flask, request

app = Flask(__name__)


@app.route('/logger', methods=["POST"])
def log_server_func():
    try:
        records = request.form.to_dict()
        log_record = logging.makeLogRecord(records)
        with open('app.log', mode='a') as file:
            file.write(str(log_record) + "\n")
        return "OK", 200
    except Exception:
        return "Error"


if __name__ == "__main__":
    app.run(debug=True, port=5555)
