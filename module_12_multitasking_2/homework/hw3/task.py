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
