import socket
import threading
from httpServer import myhttpserver

class Button(object):
    def __init__(self):

        self._pressed   = False
        self._lastValue  = self._pressed
        self._onPress   = []
        self._onRelease = []
    def pressing(self) -> bool: return self._pressed
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
    def __init__(self):
        self._value = 0
        self._onChange = []
    
    def position(self) -> float: return self._value
    def changed(self, callback: callable): self._onChange.append(callback)
    def _doCallbacks(self):
        for callback in self._onChange:
            callback()

class Controller(object):
    def __init__(self):
        self.buttonA = Button()
        self.buttonB = Button()
        self.buttonX = Button()
        self.buttonY = Button()
        self.buttonUp = Button()
        self.buttonDown = Button()
        self.buttonLeft = Button()
        self.buttonRight = Button()
        self.buttonL1 = Button()
        self.buttonL2 = Button()
        self.buttonR1 = Button()
        self.buttonR2 = Button()

        self.axis1 = Axis()
        self.axis2 = Axis()
        self.axis3 = Axis()
        self.axis4 = Axis()

class ControllerServer(object):
    def __init__(self, hostIp: str, hostPort: int):
        self.hostIp   = hostIp
        self.hostPort = hostPort

        self.controller = None

        self.buttonNames = ['buttonA', 'buttonB', 'buttonX', 'buttonY', 'buttonUp', 'buttonDown', 'buttonLeft', 
                            'buttonRight', 'buttonL1', 'buttonL2', 'buttonR1', 'buttonR2']
        self.axisNames = ['axis1', 'axis2', 'axis3', 'axis4']

        self.server = myhttpserver.Server(__name__, hostIp, hostPort)
        self.server.routes.append(('/', self.index))
        self.server.routes.append(('/setvar/<name>/<value>', self.setvar))
        threading.Thread(target=self.server.run).start()
    
    def index(self) -> str:
        with open('data/static/controller.html', 'r') as f:
            return f.read()
    
    def setvar(self, name: str, value: str):
        print(f"[VexEmulator(Controller)] {name}={value}")
        if name in self.buttonNames and self.controller != None:
            self.controller.__getattribute__(name)._pressed = value.strip().lower() == 'true'
            threading.Thread(target=self.controller.__getattribute__(name)._doCallbacks).start()
        elif name in self.axisNames and self.controller != None:
            self.controller.__getattribute__(name)._value = float(value)
            threading.Thread(target=self.controller.__getattribute__(name)._doCallbacks).start()

        return 'OK'
    
    def set_controller(self, controller: Controller):
        self.controller = controller