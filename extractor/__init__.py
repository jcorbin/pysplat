from pyparsing import *
from term import ExtractorTerm

class ExtractorPipe(object):
    def __init__(self, extractors):
        self.extractors = tuple(extractors)

    def __repr__(self):
        return '%s(%r)' % (
            self.__class__.__name__,
            self.extractors)

    def __call__(self, s):
        for extractor in self.extractors:
            s = extractor(s)
            if s is None: return None
        return s

    parse_expression = delimitedList(ExtractorTerm, delim='|')
    parse_expression.setParseAction(lambda toks: ExtractorPipe(toks))

def parse(string):
    return ExtractorPipe.parse_expression.parseString(string)
