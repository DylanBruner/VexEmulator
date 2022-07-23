class DigitalOut(object):
    def __init__(self):
        self._attributes = {
            'value': {'type': 'bool', 'value': False},   
        }
    
    def set(self, value: bool): self._attributes['value']['value'] = value