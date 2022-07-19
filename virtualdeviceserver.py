import threading, json
from vexbrain import Brain
from httpServer import myhttpserver
from vexdevices import virtualcontroller

class VirtualInterface(object):
    def __init__(self, addr: tuple, brain: Brain):
        self.server = myhttpserver.Server(name=__name__, 
                                          host=addr[0], port=addr[1])
        self.brain  = brain

        self.server.routes.append(('/', self.index))
        self.server.routes.append(('/index.js', self.indexJs))
        self.server.routes.append(('/index.css', self.indexCss))
        self.server.routes.append(('/api/devices', self.listDevices))
        self.server.routes.append(('/api/device/attributes/<deviceId>', self.listDeviceAttributes))
        self.server.routes.append(('/api/device/setattribute/<deviceId>/<attribute>/<value>', self.setDeviceAttribute))

        threading.Thread(target=self.server.run).start()

    def index(self) -> str:
        with open('data/static/index.html', 'r') as f: return f.read()
    def indexJs(self) -> str:
        with open('data/static/index.js', 'r') as f: return f.read()
    def indexCss(self) -> str:
        with open('data/static/index.css', 'r') as f: return f.read()

    def listDevices(self) -> dict:
        return json.dumps({'devices': [{'name': device._name, 'type': device._type, 'id': device._id} for device in self.brain.virtualDevices]})
    
    def listDeviceAttributes(self, deviceId: str) -> dict:
        for device in self.brain.virtualDevices:
            if device._id == deviceId:
                return json.dumps(device._attributes)

        return json.dumps({'attributes': {}})
    
    def setDeviceAttribute(self, deviceId, attribute, value):
        for device in self.brain.virtualDevices:
            if device._id == deviceId:
                if device._attributes[attribute]['type'] == 'bool':
                    device._attributes[attribute]['value'] = value.lower().strip() == 'true'
                elif device._attributes[attribute]['type'] == 'int':
                    device._attributes[attribute]['value'] = int(value)
                elif device._attributes[attribute]['type'] == 'float':
                    device._attributes[attribute]['value'] = float(value)
                elif device._attributes[attribute]['type'] == 'tuple':
                    device._attributes[attribute]['value'] = tuple(value)
                elif device._attributes[attribute]['type'] == 'str':
                    device._attributes[attribute]['value'] = str(value)
                return json.dumps({'success': True})
        return json.dumps({'success': False})