import os
from argparse import ArgumentParser
from multiprocessing.managers import SyncManager

from rotate.utils import fopen

def main():
    parser = ArgumentParser()
    parser.add_argument('-a', '--address', default='127.0.0.1:50000')
    parser.add_argument('-f', '--filename')
    args = parser.parse_args()

    host, _, port = args.address.partition(':')
    port = int(port)
    SyncManager.register('get_lock')
    SyncManager.register('get_infile')
    manager = SyncManager((host, port), authkey=b'test')
    manager.connect()
    lock = manager.get_lock()

    outfile = str(manager.get_infile())[1:-1]
    print(outfile)

    lock.acquire()
    os.rename(outfile, '{}.bak'.format(outfile))
    with fopen(outfile, 'wt') as f, fopen(args.filename, 'rt') as g:
        for line in g:
            f.write(line)
    lock.release()
