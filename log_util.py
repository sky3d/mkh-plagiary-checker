from datetime import datetime
import logging
from logging import StreamHandler
from logging import FileHandler

logger = logging.getLogger('haiku-checker')
logger.setLevel(logging.INFO)
logger.addHandler(StreamHandler())

name = datetime.now().strftime('haiku-checker_%Y-%m-%d-%H-%M.log')
name = 'haiku-checker_results_all.log'
log_file = FileHandler(name)
logger.addHandler(log_file)

logger.setLevel(level=logging.INFO)


def set_log_level(level):
    if level:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.INFO)


def log_info(s=None):
    logger.info(s)


def log_debug(s):
    logger.debug(s)


def log_error(s):
    logger.error(s)
