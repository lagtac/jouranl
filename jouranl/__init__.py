from datetime import date
import logging
from os.path import join
from os import getenv

JOURNAL_PATH = join(getenv('HOME'), '.journal')
TODAY_PATH = join(JOURNAL_PATH, date.today().isoformat())
LIST_DATA_FILE = join(JOURNAL_PATH, 'list.pickle')
HAIKU_MODE = True


def get_logger():
    ''' Get logger '''
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    fmt = logging.Formatter(
        '''%(asctime)s;%(levelname)s;%(filename)s:%(lineno)d;%(funcName)s;%(message)s''')
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger


logger = get_logger()
