from pipe import ExtractorPipe

def parse(string):
    return ExtractorPipe.parse_expression.parseString(string)
