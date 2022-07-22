class LargestObject(object):
    def __init__(self, id: str, originX: float, originY: float, centerX: float, centerY: float, width: float, height: float, angle: float, exists: bool):
        self.id      = id
        self.originX = originX
        self.originY = originY
        self.centerX = centerX
        self.centerY = centerY
        self.width   = width
        self.height  = height
        self.angle   = angle
        self.exists  = exists

            

class Vision(object):
    def __init__(self):
        self._attributes = {
            {'type': 'float',  'name': 'width',   'value': 0.0},
            {'type': 'float',  'name': 'height',  'value': 0.0},
            {'type': 'flaot',  'name': 'angle',   'value': 0.0},
            {'type': 'bool',   'name': 'exists',  'value': False},
            {'type': 'float',  'name': 'originX', 'value': 0.0},
            {'type': 'float',  'name': 'originY', 'value': 0.0},
            {'type': 'float',  'name': 'centerX', 'value': 0.0},
            {'type': 'float',  'name': 'centerY', 'value': 0.0},
            {'type': 'string', 'name': 'id',      'value': ''}
        }
    
    def get_largest_object(self) -> LargestObject:
        return LargestObject(
            id      = self._attributes['id'],
            originX = self._attributes['originX'],
            originY = self._attributes['originY'],
            centerX = self._attributes['centerX'],
            centerY = self._attributes['centerY'],
            width   = self._attributes['width'],
            height  = self._attributes['height'],
            angle   = self._attributes['angle'],
            exists  = self._attributes['exists']
        )
    
    def take_snapshot(self, signature) -> None: pass