from datetime import datetime
from threading import Lock


def convert_to_datetime(param_value):
    if param_value == "" or param_value == "-":
        return "-"

    return datetime.strptime(
        param_value.replace("T", " ").replace("+00:00", ""),
        "%Y-%m-%d %H:%M:%S",
    )


def get_basic_value(base, value):
    if base and value in base:
        return base[value]
    return '-'


def get_value(base, prop, value):
    if prop in base:
        return get_basic_value(base[prop], value)
    return '-'


class Progress:

    def __init__(self, callback, total):
        self.lock = Lock()
        self.current = 0
        self.total = total
        self.callback = callback

    def increment(self):
        self.lock.acquire()
        self.current += 1
        self.callback(self.current, self.total)
        self.lock.release()
