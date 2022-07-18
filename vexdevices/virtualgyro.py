class Gyro(object):
    def __init__(self):
        self._heading  = 0.0
        self._rotation = 0.0

    def calibrate(self): pass
    def heading(self, units) -> float: return self._heading
    def rotation(self, units) -> float: return self._rotation
    def set_heading(self, heading, units): self._heading = heading
    def set_rotation(self, rotation, units): self._rotation = rotation