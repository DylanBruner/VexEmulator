class Magnet(object):
    def __init__(self):
        self._attributes = {
            'power': {'type': 'float', 'value': 100},
            'item_picked_up': {'type': 'bool', 'value': False},
        }
    
    def set_power(self, percent): self._attributes['power']['value'] = percent
    def drop(self): self._attributes['item_picked_up']['value'] = False
    def pickup(self,duration=500): self._attributes['item_picked_up']['value'] = True