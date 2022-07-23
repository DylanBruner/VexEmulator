class Drivetrain(object):
    def __init__(self):
        self._attributes = {
            'current':     {'type': 'float', 'value': 14},
            'efficiency':  {'type': 'float', 'value': 0.8},
            'temperature': {'type': 'float', 'value': 0.0},
            'torque':      {'type': 'float', 'value': 0.0},
            'velocity':    {'type': 'float', 'value': 0.0},
            'is_done':     {'type': 'bool', 'value': True},
            'is_moving':   {'type': 'bool', 'value': False},
            'power':       {'type': 'float', 'value': 0.0},
        }

    def current(self, units): return self._attributes['current']['value']
    def drive(self, direction): pass
    def drive_for(self, direction, distance, units, wait=False): pass
    def efficiency(self): return self._attributes['efficiency']['value']
    def is_done(self): return self._attributes['is_done']['value']
    def is_moving(self): return self._attributes['is_moving']['value']
    def power(self, units): return self._attributes['power']['value']
    def set_drive_velocity(self, velocity, units): pass
    def set_stopping(self, mode): pass
    def set_timeout(self, value, units): pass
    def set_turn_velocity(self, velocity, units): pass
    def stop(self): pass
    def temperature(self, units): return self._attributes['temperature']['value']
    def torque(self, units): return self._attributes
    def turn_for(self, direction, angle, units, wait=False): pass
    def velocity(self): return self._attributes['velocity']['value']