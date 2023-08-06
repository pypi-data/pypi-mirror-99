import os
import random
import subprocess
import tempfile
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import platform
from datetime import date
from multiprocessing import Lock
from multiprocessing.managers import SyncManager

from rotate.utils import fopen

in_progress_tag = '.in-progress'

def new_filename(default_output, pps, ext, gzip=False, bzip2=False, in_progress=False):
    hostname = platform.node()
    dirname, basename = os.path.split(default_output)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    if basename:
        basename += '.'
    timestamp = int(time.time())
    dt = date.fromtimestamp(timestamp)
    datestr = dt.strftime('%Y%m%d')
    filename = os.path.join(dirname, '{base}{host}.{date}.{time}.{pps}.{ext}'.format(
        base=basename, host=hostname, date=datestr, time=timestamp, pps=pps, ext=ext))
    if gzip:
        filename += '.gz'
    elif bzip2:
        filename += '.bz2'
    if in_progress:
        filename += in_progress_tag
    return filename

def cmd_scamper(pps, tmp, write, ftype, sccmd):
    cmd = 'sudo scamper -O {ftype} -p {pps} -c "{sccmd}" -f {infile} {write}'.format(ftype=ftype, pps=pps, sccmd=sccmd, infile=tmp, write=write)
    return cmd

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--input')
    group.add_argument('-i', '--addr', nargs='*')
    parser.add_argument('-p', '--pps', default=5000, type=int, help='Packets per second.')
    parser.add_argument('-o', '--default-output', required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-z', '--gzip', action='store_true')
    group.add_argument('-b', '--bzip2', action='store_true')
    parser.add_argument('--remote')
    parser.add_argument('--cycles', type=int, default=1)
    parser.add_argument('--random', action='store_true')
    parser.add_argument('-O', '--extension', choices=['warts', 'json'], default='json')
    parser.add_argument('--in-progress', action='store_true', help='Mark file in progress with .in-progress')
    parser.add_argument('--address', default='127.0.0.1:50000')
    parser.add_argument('--debug', type=int)
    args, remaining = parser.parse_known_args()

    host, _, port = args.address.partition(':')
    port = int(port)
    lock = Lock()
    infile = args.input
    SyncManager.register('get_lock', callable=lambda: lock)
    SyncManager.register('get_infile', callable=lambda: infile)
    manager = SyncManager((host, port), authkey=b'test')
    manager.start()
    # infile = manager.Namespace()
    # infile.infile = args.input

    try:
        sccmd = ' '.join(remaining)

        cycle = 0
        while args.cycles == 0 or cycle < args.cycles:
            f = tempfile.NamedTemporaryFile(mode='wt', delete=False)
            tmp = f.name
            try:
                if args.input:
                    with lock:
                        time.sleep(30)
                        with fopen(args.input, 'rt') as g:
                            for line in g:
                                if args.random:
                                    addr, _, _ = line.rpartition('.')
                                    addr = '{}.{}'.format(addr, random.randint(0, 255))
                                else:
                                    addr = line.strip()
                                f.write('{}\n'.format(addr))
                else:
                    f.writelines('{}\n'.format(addr) for addr in args.addr)
                f.close()

                ftype = args.extension
                filename = new_filename(args.default_output, args.pps, ftype, gzip=args.gzip, bzip2=args.bzip2, in_progress=args.in_progress)
                if args.gzip:
                    write = '| gzip > {}'.format(filename)
                elif args.bzip2:
                    write = '| bzip2 > {}'.format(filename)
                else:
                    write = '-o {}'.format(filename)
                cmd = cmd_scamper(args.pps, tmp, write, ftype, sccmd)
                print(cmd)
                if args.debug:
                    with fopen(filename, 'wt') as f:
                        f.write(cmd + '\n')
                    time.sleep(args.debug)
                else:
                    start = time.time()
                    subprocess.run(cmd, shell=True, check=False)
                    end = time.time()
                    secs = end - start
                    mins = secs / 60
                    hours = mins / 60
                    print('Duration: {:,.2f} s {:,.2f} m {:,.2f} h'.format(secs, mins, hours))
                if args.in_progress:
                    os.rename(filename, filename[:-len(in_progress_tag)])
                try:
                    cycle += 1
                except OverflowError:
                    cycle = 1
            finally:
                os.unlink(tmp)
    finally:
        manager.shutdown()
