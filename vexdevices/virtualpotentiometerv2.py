class PotentiometerV2(object):
    def __init__(self) -> None:
        self._attributes = {
            'angle': {'type': 'float', 'value': 0, 'range': [0, 330]},
        }
    
    def angle(self) -> float: return self._attributes['angle']['value']