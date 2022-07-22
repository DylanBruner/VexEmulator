class Servo(object):
    def __init__(self):
        self._attributes = {
            'position': {'type': 'int', 'value': 0, 'range': [-50, 50]},
        }
    
    def set_position(self, value, units): self._attributes['position']['value'] = value