"""
Напишите Flask POST endpoint /calculate,
который принимает на вход арифметическое выражение и
вычисляет его с помощью eval (о безопасности думать не нужно,
работайте только над фукнционалом).

Поскольку наш Flask endpoint работает с арифметическими выражениями,
напишите 4 error_handler-а, которые будет обрабатывать
ArithmeticError, ZeroDivisionError, FloatingPointError и OverflowError
(о значении этих исключений вы можете посмотреть
вот на этой страничке https://docs.python.org/3/library/exceptions.html ).

Напишите по unit-тесту на каждую ошибку: тест должен проверять, что ошибка обрабатывается

Примечание: рекомендуется обрабатывать  ArithmeticError,
перехватывая InternalServerError ,
остальные классы ошибок можно обрабатывать напрямую.
"""
