class Optical(object):
    def __init__(self):
        self._attributes = {
            'brightness': {'type': 'int', 'value': 50},
            'color':      {'type': 'tuple', 'value': (0, 0, 0)},
            'gesture_on': {'type': 'bool', 'value': True},
        }

        self._gesture_left_callbacks  = []
        self._gesture_right_callbacks = []
        self._gesture_up_callbacks    = []
        self._gesture_down_callbacks  = []
        self._gesture_object_detected_callbacks = []
        self._object_lost_callbacks   = []
    
    def brightness(self) -> int: return self._attributes['brightness']['value']
    def color(self) -> tuple: return self._attributes['color']['value']
    def gesture_disable(self): self._guesture_on = False
    def gesture_enable(self):  self._guesture_on = True
    def gesture_left(self, callback: callable):    self._gesture_left_callbacks.append(callback)
    def gesture_right(self, callback: callable):   self._gesture_right_callbacks.append(callback)
    def gesture_up(self, callback: callable):      self._gesture_up_callbacks.append(callback)
    def gesture_down(self, callback: callable):    self._gesture_down_callbacks.append(callback)
    def get_gesture(self): return None
    def hue(self): return self._attributes['color']['value'][0]
    def is_near_object(self): return False
    def object_detected(self, callback: callable): self._gesture_object_detected_callbacks.append(callback)
    def object_lost(self, callback: callable):     self._object_lost_callbacks.append(callback)
    def set_light(self, state): pass
    def set_light_power(self, percent): pass
