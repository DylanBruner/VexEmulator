class RangeFinder(object):
    def __init__(self):
        self._attributes = {
            'distance':     {'type': 'int', 'value': 0},
            'found_object': {'type': 'bool', 'value': False},
        }

    def distance(self, units) -> float: return self._attributes['distance']['value']
    def found_object(self) -> bool: return self._attributes['found_object']['value']