class Distance(object):
    def __init__(self):
        self._object_detected = False
        self._object_distance = 0
        self._object_size     = 0
        self._object_velocity = 0
    
    def is_object_detected(self) -> bool: return self._object_detected
    def object_distance(self, units) -> float: return self._object_distance
    def object_size(self) -> float: return self._object_size
    def object_velocity(self) -> float: return self._object_velocity