"""
Давайте немного отойдём от логирования.
Программист должен знать не только computer science, но и математику.
Давайте вспомним школьный курс математики.

Итак, нам нужно реализовать функцию, которая принимает на вход
list из координат точек (каждая из них - tuple с x и y).

Напишите функцию, которая определяет, лежат ли все эти точки на одной прямой или не лежат
"""
from typing import List, Tuple


def check_is_straight_line(coordinates: List[Tuple[float, float]]) -> bool:
    is_straight_line = True
    if len(coordinates) == 0:
        return False
    elif len(coordinates) < 3:
        return True
    else:
        for point in range(0, len(coordinates) - 2):
            if coordinates[point + 2][0] == coordinates[point + 1][0] == coordinates[point][0]:
                if coordinates[point + 2][1] != coordinates[point + 1][1] != coordinates[point][1]:
                    break
            elif coordinates[point + 2][1] == coordinates[point + 1][1] == coordinates[point][1]:
                is_straight_line = False
                break
            else:
                try:
                    if ((coordinates[point + 2][0] - coordinates[point][0]) /
                            (coordinates[point + 1][0] - coordinates[point][0]) !=
                            (coordinates[point + 2][1] - coordinates[point][1]) /
                            (coordinates[point + 1][1] - coordinates[point][1])):
                        is_straight_line = False
                        break
                except ZeroDivisionError:
                    is_straight_line = False
                    break
        return is_straight_line


if __name__ == "__main__":
    print(check_is_straight_line([(3.0, 2.0), (3.0, 4.0), (5.0, 6.0), (27.0, 18.0), (9.0, 10.0), (11.0, 12.0)]))
