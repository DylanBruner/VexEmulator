class Gps(object):
    def __init__(self):
        self._attributes = {
            'x_position':     {'type': 'float', 'value': 0.0},
            'y_position':     {'type': 'float', 'value': 0.0},
            'x_acceleration': {'type': 'float', 'value': 0.0},
            'y_acceleration': {'type': 'float', 'value': 0.0},
            'z_acceleration': {'type': 'float', 'value': 0.0},
            'gyro_x':         {'type': 'float', 'value': 0.0},
            'gyro_y':         {'type': 'float', 'value': 0.0},
            'gyro_z':         {'type': 'float', 'value': 0.0},
            'heading':        {'type': 'float', 'value': 0.0},
            'orientation':    {'type': 'float', 'value': 0.0},
            'quality':        {'type': 'float', 'value': 0.8},
        }

        self._on_change_callbacks = []

    def acceleration(self, axis: str) -> float:
        if axis == 'xaxis': return self._attributes['x_acceleration']['value']
        if axis == 'yaxis': return self._attributes['y_acceleration']['value']
        if axis == 'zaxis': return self._attributes['z_acceleration']['value']
    
    def calibrate(self): pass 
    def changed(self, callback: callable): self._on_change_callbacks.append(callback)
    def gyro_rate(self, axis, units):
        if axis == 'xaxis': return self._attributes['gyro_x']['value']
        if axis == 'yaxis': return self._attributes['gyro_y']['value']
        if axis == 'zaxis': return self._attributes['gyro_z']['value']
    
    def heading(self): return self._attributes['heading']['value']
    def orientation(self): return self._attributes['orientation']['value']
    def quality(self): return self._attributes['quality']['value']
    def set_location(self, x, y, distance_units, heading, heading_orientation, *args):
        self._attributes['x_position']['value']  = x
        self._attributes['y_position']['value']  = y
        self._attributes['heading']['value']     = heading
        self._attributes['orientation']['value'] = heading_orientation
    def set_origin(self, x, y):
        self._attributes['x_position']['value']  = x
        self._attributes['y_position']['value']  = y
    
    def x_position(self): return self._attributes['x_position']['value']
    def y_position(self): return self._attributes['y_position']['value']