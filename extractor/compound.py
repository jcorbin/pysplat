from collections import Sequence
from common import strtuple

class CompoundExtractor(tuple):
    def extract(self, s):
        for extractor in self:
            yield extractor(s)

    def __call__(self, s):
        return strtuple(self.extract(s))

class FlatCompoundExtractor(CompoundExtractor):
    def extract(self, s):
        for extractor in self:
            yield extractor(s)

    def extract(self, s):
        for extractor in self:
            v = extractor(s)
            if isinstance(v, Sequence) and not isinstance(v, basestring):
                for i in v:
                    yield i
            else:
                yield v
