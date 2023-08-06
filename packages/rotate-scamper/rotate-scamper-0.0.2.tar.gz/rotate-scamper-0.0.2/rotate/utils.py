import bz2
import gzip
import os
import platform
import time
from datetime import date

def fopen(filename, mode='rt', *args, **kwargs):
    if filename.endswith('.gz'):
        return gzip.open(filename, mode, *args, **kwargs)
    elif filename.endswith('.bz2'):
        return bz2.open(filename, mode, *args, **kwargs)
    return open(filename, mode, *args, **kwargs)

def new_filename(default_output, proto, pps, ext, gzip=False, bzip2=False):
    hostname = platform.node()
    dirname, basename = os.path.split(default_output)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    if basename:
        basename += '.'
    timestamp = int(time.time())
    dt = date.fromtimestamp(timestamp)
    datestr = dt.strftime('%Y%m%d')
    filename = os.path.join(dirname, '{base}{host}.{date}.{time}.{proto}.{pps}.{ext}'.format(
        base=basename, host=hostname, date=datestr, time=timestamp, proto=proto, pps=pps, ext=ext))
    if gzip:
        filename += '.gz'
    elif bzip2:
        filename += '.bz2'
    return filename