from pyparsing import *
from regex import RegexExtractor
from field import FieldExtractor

pylambda = Combine(
    'lambda' + White(' ') +
    Word(alphas, alphanums) + ':' +
    CharsNotIn('|'))
pylambda.setParseAction(lambda toks: eval(toks[0]))

ExtractorTerm = pylambda | \
    FieldExtractor.parse_expression | \
    RegexExtractor.parse_expression
