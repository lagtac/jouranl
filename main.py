#! /usr/bin/env python3
''' Journal '''
import argparse
from sys import argv
import os
from os.path import join, exists
import logging
from datetime import datetime, date, time
import sqlite3

JOURNAL_PATH = join(os.getenv('HOME'), '.journal')
TODAY_PATH = join(JOURNAL_PATH, date.today().isoformat())


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

ap = argparse.ArgumentParser(description='Note-taking program')
asp = ap.add_subparsers(help='commands', dest='command')
wp = asp.add_parser('write',  help='Write an entry')
wp.add_argument('entry', nargs='+')

# exit(0)


def init():
    ''' 
    Initialize journal. Create root and today path if nesesary
    '''
    if not exists(TODAY_PATH):
        os.makedirs(TODAY_PATH, exist_ok=False)
        logger.debug('Create today path: %s', TODAY_PATH)


def write(entry):
    '''Write entry to a new file'''
    today = date.today().isoformat()
    today_filename = join(TODAY_PATH, '.'.join([today, 'txt']))
    with open(today_filename, 'a') as f:
        logger.debug('Open today file: %s', today_filename)
        f.write(entry + '\n')


def main(args):
    init()
    if args.command == 'write':
        write(' '.join(args.entry))
        #print(args.entry)
        logger.debug('Write entry in file: %s', TODAY_PATH)


if __name__ == '__main__':
    logger.debug('Starting the journal.')
    args = ap.parse_args()
    main(args)
