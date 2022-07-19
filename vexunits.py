class DummyClass(object):
    def __init__(self, values):
        for value in values: self.__setattr__(value[0], value[1])
            
new_globals = {
    'SECONDS': 'seconds',
    'MSEC': 'msec',
    'HOLD': 'hold',
    'BRAKE': 'brake',
    'COAST': 'coast',
    'FORWARD': 'forward',
    'BACKWARD': 'backward',
    'PERCENT': 'percent',
    'REVERSE': 'reverse',
    'AMP': 'amp',
    'VOLT': 'volt',
    'DEGREES': 'degrees',
    'MM': 'mm',
    'RIGHT': 'right',
    'LEFT': 'left',
    'INCHES': 'inches',
    'AxisType':        DummyClass([('XAXIS', 'xaxis'), ('YAXIS', 'yaxis'), ('ZAXIS', 'zaxis')]),
    'VelocityUnits':   DummyClass([('DPS', 'dps'), ('RPM', 'rpm'), ('DEGREES', 'degrees')]),
    'OrientationType': DummyClass([('PITCH', 'pitch'), ('ROLL', 'roll'), ('YAW', 'yaw')]),
    'XAXIS': 'xaxis',
    'YAXIS': 'yaxis',
    'ZAXIS': 'zaxis',
    'DPS': 'dps',
    'RPM': 'rpm',
    'DEGREES': 'degrees',
    'PITCH': 'pitch',
    'ROLL': 'roll',
    'YAW': 'yaw',
}