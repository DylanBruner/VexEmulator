class Rotation(object):
    def __init__(self):
        self._attributes = {
            'angle':    {'type': 'float', 'value': 0},
            'velocity': {'type': 'float', 'value': 0},
            'position': {'type': 'float', 'value': 0},
        }
    
    def angle(self) -> float: return self._attributes['angle']['value']
    def position(self, units) -> float: return self._attributes['position']['value']
    def velocity(self, units) -> float: return self._attributes['velocity']['value']
    def set_position(self, position, units): self._attributes['position']['value'] = position