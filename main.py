#! /usr/bin/env python3
''' Journal '''
from sys import argv
from os import getlogin, getenv, mkdir
from os.path import join, exists
import logging
import datetime

JOURNAL_PATH = join(getenv('HOME'), '.journal')


def get_logger():
    ''' Initialize '''
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    fmt = logging.Formatter("\
    %(asctime)s - %(levelname)s - \
    %(filename)s:%(lineno)d - \
    %(funcName)s - %(message)s \
    ")

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    return logger


logger = get_logger()


def init():
    if not exists(JOURNAL_PATH):
        logger.debug('Create journal in path: %s', JOURNAL_PATH)
        mkdir(JOURNAL_PATH)


def main(args):
    pass


if __name__ == '__main__':
    logger.debug('Hi')
    main(argv)
