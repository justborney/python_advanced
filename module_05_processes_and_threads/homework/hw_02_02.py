from pathlib import Path


class ExcListManager:
    def __init__(self, path: str, mode: str, exc_set=None):
        if exc_set is None:
            exc_set = set()
        self.exc_set = exc_set
        self.name = path
        self.mode = mode

    def __enter__(self):
        self.file = open(self.name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type in self.exc_set:
            self.file.close()
            return True
        else:
            self.file.close()


def exc_cont_manager(exceptions):
    file_path = Path(Path(__file__).parent.parent, 'homework', 'some.txt')
    try:
        with ExcListManager(str(file_path), 'r', exceptions) as f:
            f.undefined('Hello')
    except Exception as exc:

        return exc.args[0]
