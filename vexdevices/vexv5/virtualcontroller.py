class Button(object):
    def __init__(self, buttonName, controller):
        self._buttonName = buttonName
        self._controller = controller

        self._lastValue = False
        self._onPress   = []
        self._onRelease = []

    def pressing(self) -> bool: return self._controller._attributes[self._buttonName]['value']
    def pressed(self, callback: callable): self._onPress.append(callback)
    def released(self, callback: callable): self._onRelease.append(callback)

    def _doCallbacks(self):
        if not self._pressed and self._lastValue:
            self._lastValue = self._pressed
            for callback in self._onRelease:
                callback()
        elif self._pressed and not self._lastValue:
            self._lastValue = self._pressed
            for callback in self._onPress:
                callback()

class Axis(object):
    def __init__(self, axisName, controller):
        self._axisName  = axisName
        self.controller = controller
        
        self._onChange = []
    
    def position(self) -> float: return self.controller._attributes[self._axisName]['value']
    def changed(self, callback: callable): self._onChange.append(callback)
    def _doCallbacks(self):
        for callback in self._onChange:
            callback()

class Controller(object):
    def __init__(self):
        self.buttonA = Button('buttonA', self)
        self.buttonB = Button('buttonB', self)
        self.buttonX = Button('buttonX', self)
        self.buttonY = Button('buttonY', self)
        self.buttonUp = Button('buttonUp', self)
        self.buttonDown = Button('buttonDown', self)
        self.buttonLeft = Button('buttonLeft', self)
        self.buttonRight = Button('buttonRight', self)
        self.buttonL1 = Button('buttonL1', self)
        self.buttonL2 = Button('buttonL2', self)
        self.buttonR1 = Button('buttonR1', self)
        self.buttonR2 = Button('buttonR2', self)

        self.axis1 = Axis('axis1', self)
        self.axis2 = Axis('axis2', self)
        self.axis3 = Axis('axis3', self)
        self.axis4 = Axis('axis4', self)

        self._attributes = {
            'buttonA': {'type': 'bool', 'value': False},
            'buttonB': {'type': 'bool', 'value': False},
            'buttonX': {'type': 'bool', 'value': False},
            'buttonY': {'type': 'bool', 'value': False},
            'buttonUp': {'type': 'bool', 'value': False},
            'buttonDown': {'type': 'bool', 'value': False},
            'buttonLeft': {'type': 'bool', 'value': False},
            'buttonRight': {'type': 'bool', 'value': False},
            'buttonL1': {'type': 'bool', 'value': False},
            'buttonL2': {'type': 'bool', 'value': False},
            'buttonR1': {'type': 'bool', 'value': False},
            'buttonR2': {'type': 'bool', 'value': False},
            'axis1': {'type': 'float', 'value': 0},
            'axis2': {'type': 'float', 'value': 0},
            'axis3': {'type': 'float', 'value': 0},
            'axis4': {'type': 'float', 'value': 0},
        }