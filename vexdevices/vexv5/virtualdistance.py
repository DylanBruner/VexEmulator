class Distance(object):
    def __init__(self):
        self._attributes = {
            'object_detected': {'type': 'bool', 'value': False},
            'object_distance': {'type': 'float', 'value': 0},
            'object_size':     {'type': 'float', 'value': 0},
            'object_velocity': {'type': 'float', 'value': 0},
        }
    
    def is_object_detected(self) -> bool: return self._attributes['object_detected']['value']
    def object_distance(self, units) -> float: return self._attributes['object_distance']['value']
    def object_size(self) -> float: return self._attributes['object_size']['value']
    def object_velocity(self) -> float: return self._attributes['object_velocity']['value']