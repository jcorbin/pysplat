from collections import OrderedDict

class LRUOrderedDict(OrderedDict):
    maxsize = 128

    def __init__(self, _maxsize=None, *args, **kwds):
        if _maxsize is not None: self.maxsize = _maxsize
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

import errno
import fcntl
import resource

def get_nofile_avail():
    nofile = n = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
    for fd in range(0, nofile):
        try:
            fcntl.fcntl(fd, fcntl.F_GETFD)
            n -= 1
        except IOError as err:
            if err.errno != errno.EBADF:
                raise err
    return n

class LRUFileCache(LRUOrderedDict):
    has_custom_maxsize = False
    opener = lambda path: open(path, 'a')

    def __init__(self, _opener=None, _maxsize=None, *args, **kwds):
        if _maxsize is not None:
            self.maxsize = _maxsize
            self.has_custom_maxsize = True
        if _opener is not None: self.opener = _opener
        super(LRUFileCache, self).__init__(*args, **kwds)

    def use(self, key, loduse=LRUOrderedDict.use):
        try:
            return loduse(self, key)
        except KeyError:
            self[key] = fp = self.opener(key)
            return fp

    def __delitem__(self, key, delitem=OrderedDict.__delitem__):
        fp = self[key]
        delitem(self, key)
        fp.close()

    def clear(self):
        for fp in dict.itervalues(self):
            fp.close()
        OrderedDict.clear(self)

    def __del__(self):
        for fp in dict.itervalues(self):
            fp.close()

    def __enter__(self):
        if not self.has_custom_maxsize:
            self._maxsize = get_nofile_avail()-1
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clear()
