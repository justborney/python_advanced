"""
Ещё раз рассмотрим Flask endpoint, принимающий код на питоне и исполняющий его.
1. Напишите для него Flask error handler,
    который будет перехватывать OSError и писать в log файл exec.log
    соответствую ошибку с помощью logger.exception
2. Добавьте отдельный exception handler
3. Сделайте так, что в случае непустого stderr (в программе произошла ошибка)
    мы писали лог сообщение с помощью logger.error
4. Добавьте необходимые debug сообщения
5. Инициализируйте basicConfig для записи логов в stdout с указанием времени
"""
import logging
import shlex
import subprocess

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired

app = Flask(__name__)

logger = logging.getLogger("handler_logging")


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(default=10)


def run_python_code_in_subprocess(code: str, timeout: int) -> str:
    try:
        command = f'python9 -c "{code}"'
        command = shlex.split(command)
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        logger.error('OS Error was registered')
        raise exc

    outs, errs = process.communicate(timeout=timeout)

    if process.returncode != 0:
        logger.error('Error was registered')

    return outs.decode()


@app.route("/run_code", methods=["POST"])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data
        stdout = run_python_code_in_subprocess(code=code, timeout=timeout)
        return f"Stdout: {stdout}"

    return f"Bad request. Error = {form.errors}", 400


@app.errorhandler(OSError)
def handle_exception(e: OSError):
    logging.basicConfig(level='ERROR', filename='exec.log', filemode='a',
                        format='%(asctime)s, OS Error', datefmt='%H:%M:%S')
    return 'OS Error', 500


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False

    app.run(debug=True)
