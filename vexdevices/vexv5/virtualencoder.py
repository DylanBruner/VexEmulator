class Encoder(object):
    def __init__(self):
        self._attributes = {
            'velocity': {'type': 'int', 'value': 0},
            'position': {'type': 'int', 'value': 0},
        }
    
    def velocity(self, units) -> float: return self._attributes['velocity']['value']
    def position(self, units) -> float: return self._attributes['position']['value']
    def set_position(self, value: float): self._attributes['position']['value'] = value