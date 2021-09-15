"""
Напишите  hello-world endpoint , который возвращал бы строку "Привет, <имя>. Хорошей пятницы!".
Вместо хорошей пятницы, endpoint должен уметь желать хорошего дня недели в целом, на русском языке.
Текущий день недели можно узнать вот так:
>>> import datetime
>>> print(datetime.datetime.today().weekday())
"""

import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/hello-world/<username>")
def hello_world(username: str) -> str:
    """
    Func welcomes user by username and wishes a good day of the week
        :param username: str
        :return str"""
    day_of_the_week = datetime.datetime.today().weekday()
    if day_of_the_week == 1:
        good_day_of_the_week = "Хорошего понедельника!"
    elif day_of_the_week == 2:
        good_day_of_the_week = "Хорошего вторника!"
    elif day_of_the_week == 3:
        good_day_of_the_week = "Хорошей среды!"
    elif day_of_the_week == 4:
        good_day_of_the_week = "Хорошего четверга!"
    elif day_of_the_week == 5:
        good_day_of_the_week = "Хорошей пятницы!"
    elif day_of_the_week == 6:
        good_day_of_the_week = "Хорошей субботы!"
    else:
        good_day_of_the_week = "Хорошего воскресенья!"

    return f"Привет, {username}. {good_day_of_the_week}"


if __name__ == "__main__":
    app.run(debug=True)
