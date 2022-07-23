class Motor(object):
    def __init__(self):
        self._attributes = {
            'current':    {'type': 'float', 'value': 0},
            'efficiency': {'type': 'float', 'value': 0},
            'position':   {'type': 'float', 'value': 0},
            'stopping':   {'type': 'str', 'value': 'brake'},
            'is_done':    {'type': 'bool', 'value': True},
            'is_spinning':{'type': 'bool', 'value': False},
            'temperature':{'type': 'float', 'value': 0.0},
            'torque':     {'type': 'float', 'value': 0.0},
            'velocity':   {'type': 'float', 'value': 0.0},
        }

    def current(self, current) -> int: return self._attributes['current']['value']
    def efficiency(self) -> float:     return self._attributes['efficiency']['value']
    def is_done(self) -> bool: return self._attributes['is_done']['value']
    def is_spinning(self) -> bool: return self._attributes['is_spinning']['value']
    def position(self, units) -> float: return self._attributes['position']['value']
    def set_max_torque(self, value, units): pass
    def set_position(self, position, units): self._attributes['position']['value'] = position
    def set_stopping(self, mode): self._attributes['stopping']['value'] = mode
    def set_timeout(self, value, units): pass
    def set_velocity(self, velocity, units): self._attributes['velocity']['value'] = velocity
    def spin(self, direction): self._attributes['is_spinning']['value'] = True
    def spin_for(self, direction, angle, units, wait=False): pass
    def spin_to_position(self, angle, units, wait=False): pass
    def stop(self): self._attributes['is_spinning']['value'] = False
    def temperature(self, units) -> float: return self._attributes['temperature']['value']
    def torque(self, units) -> float: return self._attributes['torque']['value']
    def velocity(self, units) -> float: return self._attributes['velocity']['value']