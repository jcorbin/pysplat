from collections import Sequence
from pyparsing import *

from common import strtuple
from pipe import ExtractorPipe

compound_term = MatchFirst([ExtractorPipe.parse_expression])
compound_expr = Suppress('(') + \
    delimitedList(compound_term, delim=',') + \
    Suppress(')')
compound_term.append(compound_expr)

@compound_expr.setParseAction
def compound_expr(toks):
    return CompoundExtractor(toks)

class CompoundExtractor(tuple):
    def extract(self, s):
        for extractor in self:
            yield extractor(s)

    def __call__(self, s):
        return strtuple(self.extract(s))

    parse_expression = compound_expr
