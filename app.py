import errno
import fileinput
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

    def records(self):
        finput = fileinput.FileInput(files=self.files,
            openhook=fileinput.hook_compressed)

        for line in finput:
            yield line.rstrip('\r\n')
