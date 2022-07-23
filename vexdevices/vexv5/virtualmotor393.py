class Motor393(object):
    def __init__(self):
        self._attributes = {
            'spinning': {'type': 'bool', 'value': False},
            'velocity': {'type': 'int', 'value': 0, 'range': [0, 100]},
        }
    
    def spin(self, direction): self._attributes['spinning']['value'] = True
    def stop(self): self._attributes['spinning']['value'] = False
    def set_velocity(self, value, units): self._attributes['velocity']['value'] = value