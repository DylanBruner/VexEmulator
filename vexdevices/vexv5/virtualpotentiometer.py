class Potentiometer(object):
    def __init_(self):
        self._attributes = {
            'angle': {'type': 'float', 'value': 0, 'range': [0, 250]},
        }
    
    def angle(self, units): return self._attributes['angle']['value']