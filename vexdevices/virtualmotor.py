class Motor(object):
    def __init__(self):
        self._attributes = {
            'current':    {'type': 'float', 'value': 0},
            'efficiency': {'type': 'float', 'value': 0},
            'position':   {'type': 'float', 'value': 0},
            'stopping':   {'type': 'str', 'value': 'brake'},
        }

    def current(self, current) -> int: return self._attributes['current']['value']
    def efficiency(self) -> float:     return self._attributes['efficiency']['value']
    def is_done(self) -> bool: return True
    def is_spinning(self) -> bool: return True
    def position(self, units) -> float: return self._attributes['position']['value']
    def set_max_torque(self, value, units): pass
    def set_position(self, position, units): self._attributes['position']['value'] = position
    def set_stopping(self, mode): self._attributes['stopping']['value'] = mode
    def set_timeout(self, value, units): pass
    def set_velocity(self, velocity, units): pass
    def spin(self, direction): pass
    def spin_for(self, direction, angle, units, wait=False): pass
    def spin_to_position(self, angle, units, wait=False): pass
    def stop(self): pass
    def temperature(self, units) -> float: return 0.0
    def torque(self, units) -> float: return 0.0
    def velocity(self, units) -> float: return 0.0