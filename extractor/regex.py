import operator
import re
from pyparsing import *
from common import strtuple

Regex_flag_map = dict(zip('ilmsxu', (
    re.I, re.L, re.M, re.S, re.X, re.U)))
Regex_flags = Optional(Word('ilmsxu'))
Regex_flags.setParseAction(lambda toks: reduce(operator.or_,
    map(Regex_flag_map.__getitem__, toks[0] if toks else []), 0))

LiteralRegex = QuotedString('/', escChar='\\') + Regex_flags
LiteralRegex.setParseAction(lambda toks: re.compile(*toks))

class RegexExtractor(object):
    def __init__(self, regex):
        self.regex = regex

    def __repr__(self):
        return '%s(re.compile(%r, %d))' % (self.__class__.__name__,
            self.regex.pattern, self.regex.flags)

    def __call__(self, s):
        if not isinstance(s, basestring): s = str(s)
        match = self.regex.search(s)
        if match:
            gs = match.groups()
            if not len(gs):
                return match.group(0)
            elif len(gs) == 1:
                return gs[0]
            else:
                return strtuple(gs)

    parse_expression = LiteralRegex.copy().setParseAction(
        lambda toks: RegexExtractor(re.compile(*toks)))
