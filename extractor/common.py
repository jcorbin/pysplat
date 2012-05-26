import os

StrTupleNonePath = '__none__'

class strtuple(tuple):
    def path_components(self):
        for part in self:
            if part is None:
                yield StrTupleNonePath
            else:
                yield str(part)

    def topath(self):
        return os.path.sep.join(self.path_components())

    def __str__(self):
        return ' '.join('' if term is None else term for term in self)
