import os

StrTupleNonePath = '__none__'

class strtuple(tuple):
    def path_components(self):
        for part in self:
            if part is None:
                yield StrTupleNonePath
            else:
                yield str(part).replace(os.path.sep, '_')

    def topath(self):
        return os.path.sep.join(self.path_components())

    def __str__(self):
        return ' '.join('' if term is None else str(term) for term in self)
