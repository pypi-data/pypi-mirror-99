from typing import Tuple


class TinyFileManagerError(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return "%s" % self.message

    def __reduce__(self) -> Tuple[type, Tuple[str]]:
        return self.__class__, (self.message,)


class Unauthorized(TinyFileManagerError):
    pass


class NetworkError(TinyFileManagerError):
    pass
