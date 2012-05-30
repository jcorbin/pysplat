from compound import CompoundExtractor
from pipe import ExtractorPipe

expr = \
    CompoundExtractor.parse_expression | \
    ExtractorPipe.parse_expression
expr.streamlined = True

def parse(string):
    return expr.parseString(string)
