class strtuple(tuple):
    def __str__(self):
        return ' '.join('' if term is None else term for term in self)
