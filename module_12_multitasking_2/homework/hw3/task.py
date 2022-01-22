# import logging
# import sys
# import threading
# import time
#
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# sem = threading.Semaphore()
#
#
# def fun1(event: threading.Event):
#     logger.info('Start function fun1')
#     while not event.is_set():
#         sem.acquire()
#         print(1)
#         sem.release()
#         time.sleep(0.25)
#     logger.info('Exit from function fun1')
#
#
# def fun2(event: threading.Event):
#     logger.info('Start function fun2')
#     while not event.is_set():
#         sem.acquire()
#         print(2)
#         sem.release()
#         time.sleep(0.25)
#     logger.info('Exit from function fun2')
#
#
# def main():
#     logger.info('Start function main')
#     event = threading.Event()
#
#     try:
#         t1 = threading.Thread(target=fun1, args=(event,))
#         t1.start()
#         t2 = threading.Thread(target=fun2, args=(event,))
#         t2.start()
#
#         event.wait()
#     except KeyboardInterrupt:
#         logger.info('Ctrl+C pressed. Except KeyboardInterrupt.')
#         event.set()
#         sys.exit(1)
#
#
# if __name__ == '__main__':
#     main()


import sys
import threading
import time

sem = threading.Semaphore()


def fun1():
    while True:
        try:
            sem.acquire()
            print(1)
            sem.release()
            time.sleep(0.25)
        except KeyboardInterrupt:
            sys.exit(0)


def fun2():
    while True:
        try:
            sem.acquire()
            print(2)
            sem.release()
            time.sleep(0.25)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == '__main__':
    t1 = threading.Thread(target=fun1)
    t2 = threading.Thread(target=fun2)
    t1.daemon = True
    t1.start()
    t2.start()
