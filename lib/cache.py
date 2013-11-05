import os, tempfile, pickle
from copy import deepcopy


class ModifyCache():
    def __init__(self):
        self.cache = ModifyCache.load()
        self._cache = deepcopy(self.cache)

    @staticmethod
    def load(fname = 'last_modified'):
        try:
            f = os.path.join(tempfile.gettempdir(), fname)
            return pickle.load(open(f, "rb"))
        except IOError:
            return {}

    def save(self, fname = 'last_modified'):
        f = os.path.join(tempfile.gettempdir(), fname)
        pickle.dump(self._cache, open(f, "wb"))
        self.cache = deepcopy(self._cache)

    @staticmethod
    def clear(fname = 'last_modified'):
        try:
            f = os.path.join(tempfile.gettempdir(), fname)
            os.remove(f)
        except:
            pass

    def set(self, key, val):
        if key not in self.cache or self.cache[key] != val:
            self._cache[key] = val
            return True
        return False

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        self.save()