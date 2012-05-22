import re
from pyparsing import *

from common import strtuple
from regex import LiteralRegex

default_regex = re.compile(r'\s+')

rsep = Suppress(':')

Field = Word(nums)
Field.setParseAction(lambda toks: int(toks[0])-1)

FieldRange_open_left = rsep + Field
FieldRange_open_left.setParseAction(lambda toks: (None, toks[0]))

FieldRange_open_right = Field + rsep
FieldRange_open_right.setParseAction(lambda toks: (toks[0], None))

FieldRange = Field + rsep + Field
FieldRange.setParseAction(lambda toks: (toks[0], toks[1]))

FieldSepStr = \
    QuotedString('"', escChar='\\') | \
    QuotedString("'", escChar='\\')
FieldSepStr.setParseAction(lambda toks: re.compile(re.escape(toks[0])))

FieldSep = LiteralRegex | FieldSepStr

def build_getter(index):
    if isinstance(index, int):
        start = end = index
    elif isinstance(index, tuple) and len(index) == 2:
        start, end = index
    else:
        raise ValueError('invalid index %r' % index)

    if start is None or start == 0:
        return lambda s, seps: s[0:seps[end][0]]
    elif end is None:
        return lambda s, seps: s[seps[start-1][1]:-1]
    else:
        return lambda s, seps: s[seps[start-1][1]:seps[end][0]]

class FieldExtractor(object):
    def __init__(self, indices, regex):
        self.regex = regex
        self.indices = tuple(indices)
        self.getters = tuple(build_getter(i) for i in self.indices)

    def __repr__(self):
        return '%s(%r, re.compile(%r, %d))' % (self.__class__.__name__,
            self.indices, self.regex.pattern, self.regex.flags)

    def extract(self, s):
        seps = tuple(match.span()
            for match in self.regex.finditer(s))
        for getter in self.getters:
            try:
                yield getter(s, seps)
            except IndexError:
                yield None

    def __call__(self, s):
        return strtuple('' if v is None else v
            for v in self.extract(s))

    parse_expression = Suppress('[') + delimitedList(
        FieldRange_open_left | FieldRange | FieldRange_open_right | Field
    )('indices') + Suppress(']') + Optional(FieldSep)('separator')

    @parse_expression.setParseAction
    def parse_expression(toks):
        sep = toks.get('separator', default_regex)
        return FieldExtractor(toks['indices'], sep)

