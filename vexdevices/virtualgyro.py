class Gyro(object):
    def __init__(self):
        self._attributes = {
            'heading':  {'type': 'float', 'value': 0.0},
            'rotation': {'type': 'float', 'value': 0.0},
        }

    def calibrate(self): pass
    def heading(self, units) -> float: return self._attributes['heading']['value']
    def rotation(self, units) -> float: return self._attributes['rotation']['value']
    def set_heading(self, heading, units): self._attributes['heading']['value'] = heading
    def set_rotation(self, rotation, units): self._attributes['rotation']['value'] = rotation