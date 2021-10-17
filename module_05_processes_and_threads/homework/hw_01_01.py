import subprocess
import time


def run_vim():
    vim = subprocess.Popen(
        'vim',
        stdin=subprocess.PIPE
    )

    time.sleep(5)
    vim.communicate(input=b':qa!\n')


if __name__ == '__main__':
    run_vim()
