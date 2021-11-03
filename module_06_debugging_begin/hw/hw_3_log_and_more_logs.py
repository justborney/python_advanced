"""
Логов бывает очень много. А иногда - ооооооооочень много.
Из-за этого люди часто пишут логи не в человекочитаемом,
    а в машиночитаемом формате, чтобы машиной их было обрабатывать быстрее.

Напишите функцию

def log(level: str, message: str) -> None:
    pass


которая будет писать лог  в файл skillbox_json_messages.log в следующем формате:
{"time": "<время>", "level": "<level>", "message": "<message>"}

сообщения должны быть отделены друг от друга символами переноса строки.
Обратите внимание: наше залогированное сообщение должно быть валидной json строкой.

Как это сделать? Возможно метод json.dumps поможет вам?
"""
import datetime
import json


def log(level: str, message: str) -> None:
    time_now = datetime.datetime.now().time()
    formatted_time_now = str(time_now.strftime('%H:%M:%S'))
    with open('skillbox_json_messages.log', 'a') as log_file:
        log_line = json.dumps({"time": formatted_time_now, "level": level, "message": message})
        log_file.write(log_line + '\n')
