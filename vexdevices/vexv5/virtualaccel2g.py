class Accel2G(object):
    def __init__(self):
        self._attributes = {
            'accel': {'type': 'float', 'value': 0, 'range': [-1, 1]},
        }
    
    def acceleration(self) -> float: return self._attributes['accel']['value']