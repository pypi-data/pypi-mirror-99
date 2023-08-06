import hashlib
from datetime import datetime


def ts_now_ms() -> float:
    return int(datetime.now().timestamp())


def date_now_format() -> str:
    return datetime.now().isoformat()


def md5(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()


class ObjectView(object):
    def __init__(self, data: dict):
        self.__dict__ = data
