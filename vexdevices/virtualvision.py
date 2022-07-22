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
            'id': {'type': 'string', 'value': ''},
            'originX': {'type': 'float', 'value': 0.0},
            'originY': {'type': 'float', 'value': 0.0},
            'centerX': {'type': 'float', 'value': 0.0},
            'centerY': {'type': 'float', 'value': 0.0},
            'width': {'type': 'float', 'value': 0.0},
            'height': {'type': 'float', 'value': 0.0},
            'angle': {'type': 'float', 'value': 0.0},
            'exists': {'type': 'bool', 'value': False}
        }
    
    def get_largest_object(self) -> LargestObject:
        return LargestObject(
            id      = self._attributes['id']['value'],
            originX = self._attributes['originX']['value'],
            originY = self._attributes['originY']['value'],
            centerX = self._attributes['centerX']['value'],
            centerY = self._attributes['centerY']['value'],
            width   = self._attributes['width']['value'],
            height  = self._attributes['height']['value'],
            angle   = self._attributes['angle']['value'],
            exists  = self._attributes['exists']['value']
        )
    
    def take_snapshot(self, signature) -> None: pass