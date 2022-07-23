class DigitalIn(object):
    def __init__(self):
        self._attributes = {
            'value': {'type': 'bool', 'value': False},
        }
    
    def value(self) -> bool: return self._attributes['value']['value']