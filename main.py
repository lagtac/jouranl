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
ONE_FILE_PER_ENTRY = True


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


def parse_args(args=None):
    ''' Parse cli arguments. '''
    ap = argparse.ArgumentParser(description='Note-taking program')
    sp = ap.add_subparsers(help='commands', dest='command')
    wp = sp.add_parser('write', help='Write an entry')
    wp.add_argument('entry', nargs='*', help='The text')
    wp.add_argument('-p', dest='entry2', action='append', nargs='*', help='A paragraph')
    wp.add_argument('-t', dest='entry2', action='append', nargs='*', help='A title')
    lp = sp.add_parser('list',  help='List entries')
    lp.add_argument('-a','--all', action='store_true', help='List all entries.')
    return ap.parse_args(args)

#print(parse_args())
#exit(0)

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
    ''' Main function '''
    init()
    if args.command == 'write':
        write(' '.join(args.entry))
        # print(args.entry)
        logger.debug('Write entry in file: %s', TODAY_PATH)


if __name__ == '__main__':
    logger.debug('Starting the journal.')
    main(parse_args())
