from datetime import datetime
from os.path import join
import os
from collections import namedtuple
import pathlib
from collections import defaultdict
from pprint import pprint

from . import logger, JOURNAL_PATH, TODAY_PATH, HAIKU_MODE, LIST_DATA_FILE
from . import dateparse


def init_jouranl():
    '''
    Initialize journal. Create root and today path if nesesary
    '''
    try:
        os.makedirs(TODAY_PATH, exist_ok=False)
        # logger.debug('Create today path: %s', TODAY_PATH)
        return True
    except OSError as err:
        return False


def get_meta(author, date, tags, **kwargs):
    ''' Build a metadata namedtuple used for writing metadata '''
    Meta = namedtuple('Meta', 'Author, Date, Tags', **kwargs)
    meta = Meta(
        Author=author,
        Date=date,
        Tags=tags,
        **kwargs
    )
    return meta


def _write_meta(fd, meta_obj):
    ''' Helper function. Writes meta_obj properties to file '''
    fd.writelines(['%s: %s\n' % (i[0], i[1])
                   for i in meta_obj._asdict().items() if i[1]])
    fd.write('\n')


def write_entry(entry, tags=None, meta=True):
    '''
    Write entry to a new file.
    Format is %H%M.one-two-three.txt
    '''
    now = datetime.now()
    prefix = dateparse.strftime(now, '%H%M')
    # if entry is less than max items, slicing doesn't err
    suffix = '-'.join(entry.split()[0:3])
    fname = join(TODAY_PATH, '.'.join(
        [prefix, suffix, 'txt']))

    if HAIKU_MODE:
        with open(fname, 'w') as fd:
            logger.debug('Write entry: %s', fname)
            if meta:
                # TODO Allow more properties in ctr
                metadata = get_meta(author=os.environ.get('USER'),
                                    date=now.ctime(),
                                    tags=', '.join(tags) if tags else None)
                _write_meta(fd, metadata)
            fd.write(entry)
    else:
        raise(NotImplementedError('Non-Haiku mode not implemented.'))


def list_entry_paths(when=None, since=None, until=None, fmt=None, root_path=None, as_posix=False):
    fmt = fmt or '%Y-%m-%d'
    p = pathlib.Path(root_path) if root_path else pathlib.Path(JOURNAL_PATH)
    when = dateparse.parse(when) if when else None
    since = dateparse.parse(since) if since else None
    until = dateparse.parse(until) if until else None
    entries = []
    # print(when, since, until)

    for x in p.iterdir():
        path_date = dateparse.strptime(x.name, fmt)
        if not path_date:
            continue

        if as_posix:
            x = x.absolute().as_posix()

        if not any([when, since, until]):
            entries.append(x)
        elif when:
            #print(path_date.date(), when.date())
            if path_date.date() == when.date():
                entries.append(x)
        elif since and not until:
            if path_date >= since:
                entries.append(x)
        elif since and until:
            if path_date >= since and path_date < until:
                entries.append(x)
        elif until and not since:
            if path_date < until:
                entries.append(x)
    return sorted(entries)


def list_day_entries(date_folder, as_name=False, as_posix=False):
    path = pathlib.Path(join(JOURNAL_PATH, date_folder))
    res = []
    for e in path.iterdir():
        res.append(e.name if as_name else e.as_posix() if as_posix else e)
    return res


def list_by_path(*args, **kwargs):
    as_name = kwargs.pop('as_name', False)
    as_posix = kwargs.pop('as_posix', False)
    paths = list_entry_paths(*args, **kwargs)
    entries_list = []
    for p in paths:
        entries = list_day_entries(p, as_name=as_name, as_posix=as_posix)
        if not entries:
            continue
        entries_list.append(entries)
    return entries_list


def group_by_path(*args, **kwargs):
    as_name = kwargs.pop('as_name', False)
    as_posix = kwargs.pop('as_posix', False)
    paths = list_entry_paths(*args, **kwargs)
    entries_dict = defaultdict(list)
    for p in paths:
        entries = list_day_entries(p, as_name=as_name, as_posix=as_posix)
        if not entries:
            continue
        entries_dict[p.name] = entries
    return entries_dict


# def get_by_index(grouped_entries, day_idx, entry_idx):
#     # items = [i for i in grouped_entries.items()]
#     try:
#         for idx, i in enumerate(grouped_entries.items()):
#             # print(idx,i)
#             if idx == day_idx:
#                 return i[1][entry_idx]
#     except IndexError:
#         return None


def store_list_data(entries):
    import pickle
    with open(LIST_DATA_FILE, 'wb') as fd:
        pickle.dump(entries, fd)
    # logger.debug('Pickle list entries')


def restore_list_data():
    data = None
    import pickle
    with open(LIST_DATA_FILE, 'rb') as fd:
        data = pickle.load(fd)
    # logger.debug('Unpickle list entries')
    return data


def open_files(*files):
    pass