import logging


def setup_file_logger(
    name: str, formatter: logging.Formatter, file_path: str, level: int = logging.INFO
) -> logging.Logger:
    handler = logging.FileHandler(file_path)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def setup_console_logger(
    name: str, formatter: logging.Formatter, level: int = logging.INFO
) -> logging.Logger:
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.terminator = '\r'
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger