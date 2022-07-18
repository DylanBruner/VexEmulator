import threading

class Container(object):
    def __init__(self, code: str):
        self.code = code
        self._globals = {}
    
    def set_global(self, name: str, value):
        self._globals[name] = value
    
    def merge_globals(self, newGlobals: dict):
        self._globals.update(newGlobals)
        return self._globals
    
    def execute(self):
        exec(self.code, self._globals)
    
    def threadedExecute(self):
        threading.Thread(target=self.execute).start()