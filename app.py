import errno
import io
import os
import sys

from collections import Sequence
from pyparsing import ParseException

def open_makedirs(path):
    try:
        return open(path, 'a')
    except IOError as err:
        if err.errno != errno.ENOENT: raise err
        if '/' not in path: raise err
        os.makedirs(os.path.dirname(path))
        return open(path, 'a')

class RecordWriter(io.IOBase):
    def __init__(self, buffer, output_separator):
        self.buffer = buffer
        self.output_separator = output_separator

    @property
    def name(self):
        return self.buffer.name

    @property
    def closed(self):
        return self.buffer.closed

    def fileno(self):
        self.buffer.fileno()

    def flush(self):
        self.buffer.flush()

    def isatty(self):
        self.buffer.isatty()

    def readable(self):
        return False

    def writable(self):
        return True

    def write(self, record):
        self.buffer.write(str(record) + self.output_separator)

    def close(self):
        self.buffer.close()

import extractor
from extractor.compound import FlatCompoundExtractor

import gzip
import bz2

class App(object):
    output_separator = '\n'

    @property
    def extractor(self):
        try:
            return self._extractor
        except AttributeError:
            raise AttributeError('%r extractor not set'
                % self.__class__.__name__)

    @extractor.setter
    def extractor(self, ext):
        try:
            if isinstance(ext, basestring):
                ext = extractor.parse(ext)[0]
            elif isinstance(ext, Sequence):
                ext = FlatCompoundExtractor(extractor.parse(spec)[0]
                    for spec in ext)
            self._extractor = ext

        except ParseException as exc:
            print >>sys.stderr, "Invalid extractor:", exc
            print >>sys.stderr, exc.markInputline()
            sys.exit(1)

    def openkeyfile(self, key):
        fp = open_makedirs(key.topath())
        return RecordWriter(fp, self.output_separator)

    def open_input_file(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext == '.gz':
            return gzip.GzipFile(filename, 'r')
        elif ext == '.bz2':
            return BZ2File(filename, 'r')
        else:
            return open(filename, 'r')

    def input_files(self):
        if not self.files:
            yield sys.stdin
        else:
            for path in self.files:
                self.filename = path
                yield self.open_input_file(path)
            del self.filename

    def records(self):
        for fp in self.input_files():
            for line in fp:
                yield line.rstrip('\r\n')
