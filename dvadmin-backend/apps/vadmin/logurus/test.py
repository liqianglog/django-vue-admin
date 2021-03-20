from logging import StreamHandler, getLevelName
from logging.handlers import RotatingFileHandler
from typing import Optional, IO


class MyStreamHandler(StreamHandler):

    def __init__(self, stream: Optional[IO[str]] = ...) -> None:
        print(222)
        super().__init__(stream)

    def __repr__(self):
        level = getLevelName(self.level)
        name = getattr(self.stream, 'name', '')
        #  bpo-36015: name can be an int
        name = str(name)
        if name:
            name += ' '
        print(111)
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)
class MyRotatingFileHandler(RotatingFileHandler):

    def __init__(self, filename: str, mode: str = ..., maxBytes: int = ..., backupCount: int = ...,
                 encoding: Optional[str] = ..., delay: bool = ...) -> None:
        print(4444)
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)

    def __repr__(self):
        level = getLevelName(self.level)
        print(22)
        return '<%s %s (%s)>' % (self.__class__.__name__, self.baseFilename, level)
