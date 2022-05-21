import time
from multiprocessing import Process
from pathlib import Path

import requests as requests

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def get_cat(idx: int) -> None:
    response = requests.get(URL)
    print(response.status_code)
    result = response.content
    write_to_disk(result, idx)


def write_to_disk(content: bytes, id: int) -> None:
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(content)


def main():
    processes = [Process(get_cat(i)) for i in range(CATS_WE_WANT)]
    for process in processes:
        process.start()
        process.join()
    print(len(processes))
    time_finish = time.time()
    work_time = time_finish - time_start
    print(work_time)


if __name__ == '__main__':
    time_start = time.time()
    main()
