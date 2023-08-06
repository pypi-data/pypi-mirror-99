import bz2
import gzip
import lzma
from subprocess import Popen, PIPE
from typing import Optional


def fopen(filename, mode='rt', *args, **kwargs):
    """
    Opens file for reading or writing as either gzip, bzip2, xz, or uncompressed depending on extensions.
    :param filename: name of file to read/write
    :param mode: any valid file mode for the type of file (wt, rt, wb, rb) are universal
    :param args: passthrough positional arguments
    :param kwargs: passthrough keywork arguments
    :return: opened file object
    """
    if filename.endswith('.gz'):
        return gzip.open(filename, mode, *args, **kwargs)
    elif filename.endswith('.bz2'):
        return bz2.open(filename, mode, *args, **kwargs)
    elif filename.endswith('.xz'):
        return lzma.open(filename, mode, *args, **kwargs)
    return open(filename, mode, *args, **kwargs)

class fopen2:
    read = '{} -d -c {}'
    write = '{} > {}'
    gz = 'gzip'
    bz = 'bzip2'

    def __init__(self, filename, mode='rt', *args, **kwargs):
        self.filename = filename
        self.mode = mode
        self.args = args
        self.kwargs = kwargs
        self.f = None
        self.p: Optional[Popen] = None

    def __enter__(self):
        if self.filename.endswith('.gz'):
            comp = self.gz
        elif self.filename.endswith('.bz2'):
            comp = self.bz
        else:
            self.f = open(self.filename, self.mode, *self.args, **self.kwargs)
            return self.f
        if self.mode[0] == 'r':
            cmd = self.read
            stdout = PIPE
            stdin = None
        else:
            cmd = self.write
            stdout = None
            stdin = PIPE
        cmd = cmd.format(comp, self.filename)
        if len(self.mode) > 1 and self.mode[1] == 't':
            universal_newlines = True
        else:
            universal_newlines = False
        self.p = Popen(cmd, shell=True, universal_newlines=universal_newlines, stdout=stdout, stdin=stdin)
        if stdout is not None:
            self.f = self.p.stdout
        elif stdin is not None:
            self.f = self.p.stdin
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        if self.p is not None:
            self.p.wait()
