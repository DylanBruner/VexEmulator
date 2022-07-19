import threading, json
from httpServer import myhttpserver
from vexbrain import Brain
from vexdevices import virtualcontroller

class VirtualInterface(object):
    def __init__(self, addr: tuple, brain: Brain):
        self.server = myhttpserver.Server(name=__name__, 
                                          host=addr[0], port=addr[1])
        self.brain  = brain

        self.server.routes.append(('/devices', self.listDevices))

        threading.Thread(target=self.server.run).start()

    def listDevices(self) -> dict:
        return json.dumps({'devices': [{'name': device._name, 'type': device._type, 'id': device._id} for device in self.brain.virtualDevices]})