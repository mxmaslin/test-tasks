import logging

from pathlib import Path


file_name = Path.cwd().joinpath('error.log')

logging.basicConfig(
    filename=file_name,
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('social')

fh = logging.FileHandler(file_name)
logger.addHandler(fh)

ch = logging.StreamHandler()
logger.addHandler(ch)
