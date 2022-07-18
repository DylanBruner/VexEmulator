class Motor(object):
    def __init__(self):
        self._current    = 14
        self._efficiency = 0.8
        self._position   = 0
        self._stopping   = 'brake'

    def current(self, current) -> int: return self._current
    def efficiency(self) -> float:     return self._efficiency
    def is_done(self) -> bool: return True
    def is_spinning(self) -> bool: return True
    def position(self, units) -> float: return self._position
    def set_max_torque(self, value, units): pass
    def set_position(self, position, units): self._position = position
    def set_stopping(self, mode): self._stopping = mode
    def set_timeout(self, value, units): pass
    def set_velocity(self, velocity, units): pass
    def spin(self, direction): pass
    def spin_for(self, direction, angle, units, wait): pass
    def spin_to_position(self, angle, units, wait): pass
    def stop(self): pass
    def temperature(self, units) -> float: return 0.0
    def torque(self, units) -> float: return 0.0
    def velocity(self, units) -> float: return 0.0