"""
Давайте немного вспомним Linux command line утилиты.

Напишите Flask GET endpoint, который на вход принимает флаги командной строки,
    а возвращает результат запуска команды PS с этими флагами.
    Чтобы красиво отформатировать результат вызова программы - заключите его в тэг <pre>:
        <pre>Put your text here</pre>

Endpoint должен быть по url = /ps и принимать входные значение через аргумент arg
Напомню, вызвать программу ps можно, например, вот так

    >>> import shlex, subprocess
    >>> command_str = f"ps aux"
    >>> command = shlex.split(command_str)
    >>> result = subprocess.run(command, capture_output=True)
"""
from typing import List
from flask import Flask
from flask import request
import shlex
import subprocess

app = Flask(__name__)


@app.route("/ps/", methods=["GET"])
def _ps():
    args: List[str] = request.args.getlist("args", type=str)

    flag = args[0]
    command_str = f"ps {flag}"
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True)
    return f'<pre>{result.stdout.decode()}</pre>'


if __name__ == "__main__":
    app.run(debug=True)
