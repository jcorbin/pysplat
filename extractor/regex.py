import operator
import re
from pyparsing import *

Regex_flag_map = dict(zip('ilmsxu', (
    re.I, re.L, re.M, re.S, re.X, re.U)))
Regex_flags = Optional(Word('ilmsxu'))
Regex_flags.setParseAction(lambda toks: reduce(operator.or_,
    map(Regex_flag_map.__getitem__, toks[0] if toks else []), 0))

LiteralRegex = QuotedString('/', escChar='\\') + Regex_flags
LiteralRegex.setParseAction(lambda toks: re.compile(*toks))
