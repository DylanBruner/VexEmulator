class Bumper(object):
    def __init__(self):
        self._attributes = {
            'pressed': {'type': 'bool', 'value': False},
            '_pressCallbacks': {'type': 'list', 'value': []},
            '_releasedCallbacks': {'type': 'list', 'value': []},
        }
    
    def pressing(self) -> bool: return self._attributes['pressed']['value']
    def pressed(self, callback: callable): self._attributes['_pressCallbacks']['value'].append(callback)
    def released(self, callback: callable): self._attributes['_releasedCallbacks']['value'].append(callback)