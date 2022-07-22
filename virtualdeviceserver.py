import threading, json, program
from vexbrain import Brain
from httpServer import myhttpserver

class VirtualInterface(object):
    def __init__(self, addr: tuple, brain: Brain):
        self.server = myhttpserver.Server(name=__name__, 
                                          host=addr[0], port=addr[1])
        self.brain  = brain

        self.server.routes.append(('/', self.index))
        self.server.routes.append(('/index.js', self.indexJs))
        self.server.routes.append(('/api/devices', self.listDevices))
        self.server.routes.append(('/api/device/attributes/<deviceId>', self.listDeviceAttributes))
        self.server.routes.append(('/api/device/setattribute/<deviceId>/<attribute>/<value>', self.setDeviceAttribute))
        self.server.routes.append(('/api/device/callattribute/<deviceId>/<attribute>', self.callAttribute))
        self.server.routes.append(('/api/interact/brain/<functionString>', self.interactBrain))
        self.server.routes.append(('/api/program/loadandrun/<programFile>', self.loadAndRun))

        threading.Thread(target=self.server.run).start()

    def stopServer(self): self.server.stop()

    def loadAndRun(self, programFile: str):
        #Stop any currently running program
        if self.brain.CodeEnviorment != None: self.brain.teardownProgram()
        prgm = program.ProgramFile(f'data/emulatedstorage/Internal/programs/{programFile}')

        #Get the brain ready to run the program
        self.brain.onProgramFolderScreen = False; self.brain.BrainScreen._drawProgramBar = True
        self.brain.onProgramScreen       = True;  self.brain.onHomeScreen = False
        self.brain.onDeviceScreen        = False; self.brain.BrainScreen.clear_screen()

        #Run the program
        self.brain.CodeEnviorment = prgm.loadContainer(self.brain)
        self.brain.CodeEnviorment.threadedExecute()

        return json.dumps({'success': True})

    def index(self) -> str:
        with open('data/static/index.html', 'r') as f: return f.read()
    def indexJs(self) -> str:
        with open('data/static/index.js', 'r') as f: return f.read()

    def interactBrain(self, functionString):
        try:
            threading.Thread(self.brain.__getattribute__(functionString)).start()
        except AttributeError as e:
            return json.dumps({'success': False, 'error': str(e)})
        return json.dumps({'success': True})

    def listDevices(self) -> dict:
        devices = {'devices': []}
        for device in self.brain.virtualDevices:
            devices['devices'].append({
                'name': device._name,
                'type': device._type,
                'id': device._id,
            })

        return json.dumps(devices)
    
    def callAttribute(self, deviceId, attribute):
        for device in self.brain.virtualDevices:
            if device._id == deviceId:
                threading.Thread(target=device._attributes[attribute]['value']).start()
        return json.dumps({'success': True})

    def listDeviceAttributes(self, deviceId: str) -> dict:
        attributes = {'attributes': {}}
        for device in self.brain.virtualDevices:
            if device._id == deviceId:
                for attribute in device._attributes:
                    attributeName = attribute
                    attribute = device._attributes[attribute]
                    if attribute['type'] != 'callback':
                        attributes['attributes'][attributeName] = attribute
                    else:
                        attributes['attributes'][attributeName] = {'type': attribute['type'], 'value': '(callback)'}

        return json.dumps(attributes)
    
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