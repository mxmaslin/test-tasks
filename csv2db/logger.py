from distutils.log import Log
import logging
from logging import FileHandler, Formatter, Logger, StreamHandler


from typing import Optional, Union


class Logger:
    def __init__(
        self, name: str, handler: Union[FileHandler, StreamHandler],
        formatter: Formatter, level: int = logging.INFO,
        file_path: Optional[str] = None
    ):
        self.handler = handler(file_path)
        self.handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(self.handler)
    
    def logger(self) -> Logger:
        return self.logger


class ConsoleLogger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler.terminator = '\r'


class FileLogger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
