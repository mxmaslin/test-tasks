import logging

logger = logging.getLogger('sender')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('error.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    """%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s"""
)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
