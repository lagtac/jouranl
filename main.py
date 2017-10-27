#! /usr/bin/env python3
''' Journal '''
from sys import argv
from os import getlogin, getenv, mkdir
from os.path import join, exists
import logging
from datetime import datetime, date, time
import sqlite3

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
        mkdir(JOURNAL_PATH)
        logger.debug('Create journal directory: %s', JOURNAL_PATH)
    today = str(date.today())

    if not exists(join(JOURNAL_PATH, today)):
        mkdir(join(JOURNAL_PATH, today))
        logger.debug('Create today directory: %s', JOURNAL_PATH)

    today_file = join(JOURNAL_PATH, today, '.'.join([today,'txt']))
    if not exists(today_file):
        with open(today_file, mode='w') as f:
            f.writelines(['---\n\n','---\n'])
            logger.debug('Touch today file: %s', today_file)


def write(entry):
   pass 

def main(args):
    init()


if __name__ == '__main__':
    logger.debug('Hi')
    main(argv)
