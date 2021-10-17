import subprocess


def run_program():
    subprocess.run(['python', 'test_program.py'], input='Ivanov\nIvan\n30', encoding='utf8', text=True)


if __name__ == '__main__':
    run_program()
