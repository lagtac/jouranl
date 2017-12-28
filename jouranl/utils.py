import os
import pathlib

from . import logger


def walk_entries(path, entries=None, parent=None):
    ''' Walk jouranl recursively. 
        Returns a dictionary of day_folder: entries
    '''
    path = pathlib.Path(path)
    entries = entries or {}
    if path.is_dir():
        entries[path.name] = []
        for x in path.iterdir():
            walk_entries(x, entries, path.name)
        # When you run out of dirs return the dict
        return entries
    else:
        entries[parent].append(path.name)


def open_temp_file(entry=None):
    import tempfile
    import subprocess
    with tempfile.NamedTemporaryFile(mode='w+', prefix='jouranl_') as fd:
        logger.debug('Open tempfile: %s', fd.name)
        default_editor = os.environ.get('EDITOR', 'vi')
        # TODO Open the tempfile with data already written in it
        # fd.write(entry)
        # TODO Understand how subprocess works
        completed_process = subprocess.run([default_editor, fd.name])
        fd.seek(0)
        return fd.read()


def color_print(terminfo_code, *args, **kwargs):
    os.system('tput setaf {}'.format(terminfo_code))
    flush = kwargs.pop('flush', True)
    print(*args, flush=flush, **kwargs)
    os.system('tput setaf 7')
