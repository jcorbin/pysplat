from collections import OrderedDict

class LRUOrderedDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.maxsize = kwds.pop('_maxsize', 128)
        super(LRUOrderedDict, self).__init__(*args, **kwds)

    def use(self, key, PREV=0, NEXT=1):
        value = self[key]
        link_prev, link_next, key = self._OrderedDict__map.pop(key)
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev
        root = self._OrderedDict__root
        last = root[PREV]
        last[NEXT] = root[PREV] = self._OrderedDict__map[key] = [last, root, key]
        return value

    def __setitem__(self, key, value, PREV=0, NEXT=1, KEY=2,
            setitem=OrderedDict.__setitem__):
        if key not in self and len(self) >= self.maxsize:
            oldest_key = self._OrderedDict__root[NEXT][KEY]
            del self[oldest_key]
        setitem(self, key, value)
