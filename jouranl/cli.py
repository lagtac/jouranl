#! /usr/bin/env python3
''' Journal CLI '''
import argparse
from pprint import pprint
from markdown import Markdown
from markdown.extensions.meta import MetaExtension

from . import JOURNAL_PATH, TODAY_PATH, logger
from . import api
from . import utils


def parse_args(args=None):
    ''' Parse cli arguments. '''
    ap = argparse.ArgumentParser(description='Note-taking program')
    sp = ap.add_subparsers(help='commands', dest='command')

    tp = sp.add_parser('test')
    #tp.add_argument('-t', '--test', action='store_true', nargs='+')

    wp = sp.add_parser('write', help='Write an entry')
    wp.add_argument('entry', nargs='*', help='The text')
    wp.add_argument('-e', '--editor', action='store_true')
    wp.add_argument('-m', '--meta', action='store_true')
    wp.add_argument('-t', '--tags', action='store', nargs='+')
    wp.add_argument('-i', '--interactive', action='store_true')

    lp = sp.add_parser('list',  help='List entries')
    lp.add_argument('-a', '--all', action='store_true', default=True,
                    help='List all entries.')
    lp.add_argument('-s', '--since', action='store', nargs='+')
    lp.add_argument('-u', '--until', action='store', nargs='+')
    lp.add_argument('-w', '--when', action='store', nargs='+')

    rp = sp.add_parser('read',  help='Read entries')
    # rp.add_argument('index', nargs='+')
    rp.add_argument('-i', '--indexes', dest='indexes',
                    action='append', nargs='+', type=int)

    return ap.parse_args(args)


def main():
    ''' Main function '''
    api.init_jouranl()
    args = parse_args()

    if args.command == 'test':
        pass

    if args.command == 'write':
        entry = ' '.join(args.entry)
        tags = args.tags or []
        meta = args.meta
        # Use editor

        if args.editor:
            entry = utils.open_temp_file(entry)

        if args.interactive:
            lines = []
            while(True):
                x = input('> ')
                if not x:
                    entry = '\n'.join(lines)
                    tags_prompt = input('Tags (comma separated):\n> ')
                    tags.extend([t.strip()
                                 for t in tags_prompt.split(',') if tags_prompt])
                    break
                else:
                    lines.append(x)
        if entry:
            api.write_entry(entry, tags=tags, meta=True if tags else meta)
            logger.debug('Write entry: %s', TODAY_PATH)

    if args.command == 'list':
        entries = group_by_path(args)
        api.store_list_data(entries)
        print_with_id(entries, as_name=True)

    if args.command == 'read':
        # Get entries from last list command
        entries = list(api.restore_list_data().items())
        # Create a list from selected indexes
        selected_indexes = args.indexes
        selection = []
        for index_group in selected_indexes:
            day, indexes = index_group[0], set(index_group[1:])
            if indexes:
                for idx in indexes:
                    selection.append(entries[day][1][idx])
            else:
                selection.extend(entries[day][1])

        for pp in selection:
            with pp.open() as fd:
                lines = fd.readlines()
                utils.color_print(6, pp.parent.name, '/', pp.name)
                if lines:
                    md = Markdown(extensions=[MetaExtension()])
                    lines = md.preprocessors['meta'].run(lines)
                    print(' ', ''.join(lines))
                    for k, v in md.Meta.items():
                        utils.color_print(
                            5, "  {:<10} {}".format(k + ':', ''.join(v)))
                else:
                    utils.color_print(8, '  EMPTY')
                # utils.color_print(6, '~')
                print()


def group_by_path(args):
    when = ' '.join(args.when) if args.when else None
    since = ' '.join(args.since) if args.since else None
    until = ' '.join(args.until) if args.until else None
    #entry_paths = api.list_entry_paths(when, since, until)

    entries_by_path = api.group_by_path(
        when, since, until, as_name=False)

    return entries_by_path


def print_with_id(entries_dict, as_name=False):
    for idx, p in enumerate(entries_dict.items()):
        utils.color_print(6, idx, end=' ', flush=True)
        utils.color_print(7, p[0])
        for idx2, e in enumerate(p[1]):
            utils.color_print(6, f'{"":>2}{idx2:<4}', end=' ')
            utils.color_print(7, f'{e.name if as_name else e}')


if __name__ == '__main__':
    # logger.debug('Starting the journal.')
    main()
