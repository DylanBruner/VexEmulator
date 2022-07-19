import contextlib, threading, ctypes, time

class StoppableThread(threading.Thread):
    def __init__(self, name, container):
        threading.Thread.__init__(self)
        self.name = name
        self.container = container
    
    def run(self):
        self.container.execute()
    
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    def stop(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('[VexEmulator(Container)] Stopped container')

class Container(object):
    def __init__(self, code: str):
        self.code = code
        self._globals = {}

        self.executionFailed = False
    
    def set_global(self, name: str, value):
        self._globals[name] = value
    
    def merge_globals(self, newGlobals: dict):
        self._globals.update(newGlobals)
        return self._globals
    
    def stop(self):
        self.executer.stop()

    def execute(self):
        self.set_global('container', self)
        try:
            exec(self.code, self._globals)
        except Exception as e:
            print(f'[VexEmulator(Container)/Error] {e}')
            self.executionFailed = True

    def threadedExecute(self):
        self.executer = StoppableThread('Executer', self)
        self.executer.start()