"""
Реализуйте endpoint, с url, начинающийся с  /max_number ,
в который можно будет передать список чисел, перечисленных через / .
Endpoint должен вернуть текст "Максимальное переданное число {number}",
где number, соответственно, максимальное переданное в endpoint число,
выделенное курсивом.
"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers: str) -> str:
    """
    Func returns  the largest number from the given ones
    :param numbers: str with given numbers
    :return str with the largest number form the given ones"""
    try:
        int_numbers = [int(number) for number in numbers.split('/')]
        return f'The largest number form the given ones is {max(int_numbers)}'
    except ValueError:
        return 'Wrong input'


if __name__ == "__main__":
    app.run(debug=True)
