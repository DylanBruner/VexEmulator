class Rotation(object):
    def __init__(self):
        self._angle    = 0
        self._velocity = 0
        self._position = 0
    
    def angle(self) -> float: return self._angle
    def position(self, units) -> float: return self._position
    def velocity(self, units) -> float: return self._velocity
    def set_position(self, position, units): self._position = position