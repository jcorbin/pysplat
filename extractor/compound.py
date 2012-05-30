from collections import Sequence
from common import strtuple

class CompoundExtractor(tuple):
    def extract(self, s):
        for extractor in self:
            yield extractor(s)

    def __call__(self, s):
        return strtuple(self.extract(s))
