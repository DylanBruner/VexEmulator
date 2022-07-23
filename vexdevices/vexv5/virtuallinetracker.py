class LineTracker(object):
    def __init__(self):
        self._attributes = {
            'reflectivity': {'type': 'float', 'value': 0, 'range': [0, 100]},
        }
    
    def reflectivity(self) -> int: return self._attributes['reflectivity']['value']