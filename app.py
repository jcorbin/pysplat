import errno
import io
import os
import sys

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
from extractor.compound import CompoundExtractor

import gzip
import bz2

class DerpBZ2File(bz2.BZ2File):
    def __init__(self, name, mode='r', buffering=0, compresslevel=9):
        self.name = name
        super(DerpBZ2File, self).__init__(
            name, mode, buffering, compresslevel)

class App(object):
    keyfilebase = None
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
            self._extractor = extractor.parse(ext)[0]

        except ParseException as exc:
            print >>sys.stderr, "Invalid extractor:", exc
            print >>sys.stderr, exc.markInputline()
            sys.exit(1)

    def openkeyfile(self, key):
        path = key.topath()
        if self.keyfilebase:
            path = os.path.join(self.keyfilebase, path)
        fp = open_makedirs(path)
        return RecordWriter(fp, self.output_separator)

    def open_input_file(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext == '.gz':
            return gzip.GzipFile(filename, 'r')
        elif ext == '.bz2':
            return DerpBZ2File(filename, 'r')
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

    def parse_file_records(self, fp):
        for line in fp:
            yield line.rstrip('\r\n')

    def records(self):
        for fp in self.input_files():
            for record in self.parse_file_records(fp):
                yield record
