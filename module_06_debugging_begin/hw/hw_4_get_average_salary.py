"""
Вы работаете программистом на предприятии.
К вам пришли из бухгалтерии и попросили посчитать среднюю зарплату по предприятию.
Вы посчитали, получилось слишком много, совсем не реалистично.
Вы подумали и проконсультировались со знакомым из отдела статистики.
Он посоветовал отбросить максимальную и минимальную зарплату.
Вы прикинули, получилось что-то похожее на правду.

Реализуйте функцию get_average_salary_corrected,
которая принимает на вход непустой массив заработных плат
(каждая -- число int) и возвращает среднюю з/п из этого массива
после отбрасывания минимальной и максимальной з/п.

Задачу нужно решить с алгоритмической сложностью O(N) , где N -- длина массива зарплат.

Покройте функцию логгированием.
"""
from typing import List


def get_average_salary_corrected(salaries: List[int]) -> float:
    total = sum(salaries)
    count = len(salaries)
    minimum, maximum, min_count, max_count = 0 * 4
    if len(set(salaries)) >= 3:
        for salary in salaries:
            if salary < minimum:
                minimum = salary
                min_count = 1
            elif salary == minimum:
                min_count += 1
            if salary > maximum:
                maximum = salary
                max_count = 1
            elif salary == maximum:
                max_count += 1
            total += salaries[salary]
            count += 1
    average_salary = round((total - minimum * max_count - maximum * max_count) / (count + min_count + max_count), 2)
    return average_salary
