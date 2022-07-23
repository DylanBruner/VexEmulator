class Inertial(object):
    def __init__(self):
        self._attributes = {
            'X_acceleration': {'type': 'float', 'value': 0},
            'Y_acceleration': {'type': 'float', 'value': 0},
            'Z_acceleration': {'type': 'float', 'value': 0},
            'X_gyro_rate':    {'type': 'float', 'value': 0},
            'Y_gyro_rate':    {'type': 'float', 'value': 0},
            'Z_gyro_rate':    {'type': 'float', 'value': 0},
            'heading':        {'type': 'float', 'value': 0},
            'pitch':          {'type': 'float', 'value': 0},
            'roll':           {'type': 'float', 'value': 0},
            'yaw':            {'type': 'float', 'value': 0},
            'rotation':       {'type': 'float', 'value': 0},
        }
    
    def acceleration(self, type) -> float:
        if type == 'xaxis':   return self._attributes['X_acceleration']['value']
        elif type == 'yaxis': return self._attributes['Y_acceleration']['value']
        elif type == 'zaxis': return self._attributes['Z_acceleration']['value']
    
    def calibrate(self): pass

    def gyro_rate(self, type, units):
        if type == 'xaxis':   return self._attributes['X_gyro_rate']['value']
        elif type == 'yaxis': return self._attributes['Y_gyro_rate']['value']
        elif type == 'zaxis': return self._attributes['Z_gyro_rate']['value']
    
    def heading(self, units): return self._attributes['heading']['value']
    def orientation(self, type, units):
        if type == 'pitch': return self._attributes['pitch']['value']
        elif type == 'roll': return self._attributes['roll']['value']
        elif type == 'yaw': return self._attributes['yaw']['value']
    
    def rotation(self, units): return self._attributes['rotation']['value']
    def set_heading(self, value, units):  self._attributes['heading']['value'] = value
    def set_rotation(self, value, units): self._attributes['rotation']['value'] = value