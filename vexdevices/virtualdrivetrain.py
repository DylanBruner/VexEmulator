class Drivetrain(object):
    def current(self, units): return 14
    def drive(self, direction): pass
    def drive_for(self, direction, distance, units, wait): pass
    def efficiency(self): return 0.8
    def is_done(self): return True
    def is_moving(self): return False
    def power(self, units): return 0.0
    def set_drive_velocity(self, velocity, units): pass
    def set_stopping(self, mode): pass
    def set_timeout(self, value, units): pass
    def set_turn_velocity(self, velocity, units): pass
    def stop(self): pass
    def temperature(self, units): return 0.0
    def torque(self, units): return 0.0
    def turn_for(self, direction, angle, units, wait): pass
    def velocity(self): return 0.0