from regex import RegexExtractor
from field import FieldExtractor
from pyparsing import *

pylambda = Combine(
    'lambda' + White(' ') +
    Word(alphas, alphanums) + ':' +
    CharsNotIn('|'))
pylambda.setParseAction(lambda toks: eval(toks[0]))

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
        return s

    parse_expression = delimitedList(
        pylambda |
        FieldExtractor.parse_expression |
        RegexExtractor.parse_expression,
        delim='|')
    parse_expression.setParseAction(lambda toks: ExtractorPipe(toks))
