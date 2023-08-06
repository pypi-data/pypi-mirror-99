''' LRUCache '''

from time import time
from collections import OrderedDict


class LRUCache:
    ''' LRUCache class'''

    def __init__(self, max_size, max_age):
        self._max_size = max_size
        self._max_age = max_age
        self._items = OrderedDict()

    def add(self, key, value):
        ''' Add key-value pair in cache '''
        if key in self._items:
            del self._items[key]

        self._items[key] = {
            'value': value,
            'timestamp': time()
        }
        if len(self._items) > self._max_size:
            self._items.popitem(last=False)

    def remove(self, key):
        ''' Remove element '''
        if key in self._items:
            del self._items[key]

    def get(self, key):
        ''' Get element by key or None if expired or missing '''
        if key not in self._items:
            return None
        item = self._items.pop(key)
        current_time = time()
        if current_time - item['timestamp'] >= self._max_age:
            return None
        item['timestamp'] = current_time
        self._items[key] = item
        return item['value']

    def clear(self):
        ''' Remove all elements '''
        self._items = OrderedDict()
