class Magnet(object):
    def __init__(self):
        self._power = 100
        self._item_picked_up = False
    
    def set_power(self, percent): self._power = percent
    def drop(self):   self._item_picked_up = False
    def pickup(self,duration=500): self._item_picked_up = True