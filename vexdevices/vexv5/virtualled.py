class Led(object):
    def __init__(self):
        self._attributes = {
            'state': {'type': 'bool', 'value': False},
        }
    
    def on(self): self._attributes['state']['value'] = True
    def off(self): self._attributes['state']['value'] = False