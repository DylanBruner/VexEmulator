class LimitSwitch(object):
    def __init__(self):
        self._attributes = {
            'pressed': {'type': 'bool', 'value': False},
        }
    
    def pressed(self, callback: callable): pass
    def released(self, callback: callable): pass
    def pressing(self) -> bool: return self._attributes['pressed']['value']