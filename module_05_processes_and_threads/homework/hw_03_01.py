import os.path
import sys


class StdErrOutManager:
    def __init__(self, user_file: str, mode: str, out: str, err: str, data: str):
        self.name = os.path.abspath(user_file)
        self.mode = mode
        self.original_out = sys.stdout
        self.original_err = sys.stderr
        self.out = os.path.abspath(out)
        self.err = os.path.abspath(err)
        self.data = data

    def __enter__(self):
        user_file_path = os.path.abspath(self.name)
        self.file = open(user_file_path, self.mode)
        sys.stdout = open(self.out, 'w')
        sys.stderr = open(self.err, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.data:
            sys.stderr.write('Empty data detected')
            self.file.close()
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = self.original_out
            sys.stderr = self.original_err
            return True
        else:
            self.file.write(self.data)
            sys.stdout.write('Success record')
            self.file.close()
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = self.original_out
            sys.stderr = self.original_err


if __name__ == '__main__':
    test_data = ''
    file_path = os.path.abspath('test_file.txt')
    with StdErrOutManager(file_path, 'w', 'new_out.txt', 'new_err.txt', test_data) as file:
        pass
