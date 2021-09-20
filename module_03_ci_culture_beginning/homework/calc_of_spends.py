from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int) -> str:
    """
    Func adds record of the spending
    :param date: str YYYYMMDD, MM 01 - 12, DD 01 - 31
    :param number: int spending sum
    :return: str about success recording
    """
    year = int(date[:4])
    month = int(date[4:6])
    if year in storage:
        if month in storage[year]:
            storage[year][month] += number
        else:
            storage[year][month] = number
    else:
        storage[year] = {month: number}
    return f'Spending was added'


@app.route("/calculate/<int:year>")
def calculate_year(year: int) -> str:
    """
    Func returns sum of year spending
    :param year: int
    :return: sum of year spending or message, that no records of given year
    """
    if year in storage:
        year_sum = 0
        for month in storage[year]:
            year_sum += int(calculate_month(year, month).split(' ')[-1])
        return f'Total year {year} spending is {year_sum}'
    else:
        return f'No records for year {year}'


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int) -> str:
    """
    Func returns sum of month spending
    :param year: int
    :param month: int
    :return: sum of month spending or message, that no records of given year or month
    """
    if year in storage:
        if month in storage[year]:
            return f'Total month {month} spending is {storage[year][month]}'
        else:
            return f'No records for month {month}'
    else:
        return f'No records for year {year}'


if __name__ == "__main__":
    app.run(debug=True)
