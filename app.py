#!env/bin/python

import argparse
import os
import itertools
from datetime import datetime
from operator import itemgetter

def get_times(path):
    if os.path.islink(path):
        return [0]
    yield 0
    if os.path.isfile(path):
        stat = os.stat(os.path.join(path))
        if stat:
            if stat.st_mtime:
                yield stat.st_mtime
            if stat.st_ctime:
                yield stat.st_ctime

    elif os.path.isdir(path):
        for root, files, dirs in os.walk(path):
            for p in itertools.chain(files, dirs):
                if os.path.islink(os.path.join(root, p)):
                    continue
                stat = os.stat(os.path.join(root, p))
                if stat:
                    if stat.st_mtime:
                        yield stat.st_mtime
                    if stat.st_ctime:
                        yield stat.st_ctime

def get_max_time(directory_path):
    return max(get_times(directory_path))

def get_ordered_dirs(root):
    print('Looking for %s' % root) 
    dirs = os.listdir(root)
    print('Dirs: %s' % dirs)
    with_time = [(d, get_max_time(os.path.join(root, d))) for d in dirs]
    return sorted(with_time, key=itemgetter(1))

def main():
    parser = argparse.ArgumentParser(description='Sorts a list of directories by their access/add/modification time')
    parser.add_argument('root')
    args = parser.parse_args()
    if os.path.isdir(args.root):
        ordered_dirs_with_time = get_ordered_dirs(os.path.abspath(args.root))
        for dirname, time in ordered_dirs_with_time:
            print('{time:%Y-%m-%d} - {dirname}'.format(time=datetime.fromtimestamp(time), dirname=dirname))
    else:
        raise '{root} is not a directory'.format(root=root)


if __name__ == '__main__':
    main()

