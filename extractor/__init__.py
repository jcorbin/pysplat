from regex import RegexExtractor
from field import FieldExtractor
from pyparsing import *

pylambda = Combine(
    'lambda' + White(' ') +
    Word(alphas, alphanums) + ':' +
    CharsNotIn('|'))
pylambda.setParseAction(lambda toks: eval(toks[0]))
