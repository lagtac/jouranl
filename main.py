#! /usr/bin/env python3
''' Journal '''
import argparse
from sys import argv
from os import getlogin, getenv, mkdir
from os.path import join, exists
import logging
from datetime import datetime, date, time
import sqlite3

JOURNAL_PATH = join(getenv('HOME'), '.journal')

ap = argparse.ArgumentParser(description='Note-taking program')
asp = ap.add_subparsers(help='commands')
wp = asp.add_parser('write', help='Write an entry')
wp.add_argument('-p', '--paragraph', dest='paragraph',
                action='append', nargs='*')
wp.add_argument('-t', '--title', dest='title', action='append', nargs='*')
print(ap.parse_args())
exit(0)


def get_logger():
    ''' Get logger '''
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
    today = date.today().isoformat()

    if not exists(join(JOURNAL_PATH, today)):
        mkdir(join(JOURNAL_PATH, today))
        logger.debug('Create today directory: %s', JOURNAL_PATH)

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    now_filename = '.'.join([now, 'txt'])
    # today_file = join(JOURNAL_PATH, today, '.'.join([today,'txt']))
    if not exists(now_filename):
        with open(now_filename, mode='w') as f:
            f.writelines(['---\n\n', '---\n'])
            logger.debug('Touch today file: %s', now_filename)


def write(entry):
    '''Write entry to a new file'''

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    now_filename = '.'.join([now, 'txt'])

    if not exists(now_filename):
        with open(now_filename, mode='w') as f:
            f.write(entry)
            logger.debug('Touch today file: %s', now_filename)


def main(args):
    init()


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument_group()
    logger.debug('Hi')
    main(argv)
