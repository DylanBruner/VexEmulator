class Light(object):
    def __init__(self):
        self._attributes = {
            'brightness': {'type': 'int', 'value': 0, 'range': [0, 100]},
        }