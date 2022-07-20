import time, threading, ctypes

class StoppableThread(threading.Thread):
    def __init__(self, function: callable):
        threading.Thread.__init__(self)
        self.function = function
    
    def run(self):
        self.function()
    
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

class CompetitionAttributeStore(object):
    def __init__(self, brain):
        self._attributes = {
            'driver_control':    {'value': False, 'type': 'bool'},
            'autonomous':        {'value': False, 'type': 'bool'},
            'start_competition': {'value': self.StartCompetition, 'type': 'callback'},
        }

        self.brain = brain

        self.user_control = None
        self.autonomous   = None

        self.competition_start_time = None
        self.competition_state      = None
        self.competition_thread     = None
    
    def _CompetitionLoop(self):  # sourcery skip: extract-duplicate-method
        for x in range(3, 0, -1): print(f"[VexEmulator(CompetitionController)] Starting in {x}"); time.sleep(1)
        self.competition_start_time = time.time()
        while True:
            if self.competition_state is None:
                self.competition_start_time = time.time()
                self.brain.BrainScreen.startTime = self.competition_start_time
                self.competition_state = 'autonomous'
                self._attributes['autonomous']['value'] = True
                self.competition_thread = StoppableThread(self.autonomous); self.competition_thread.start()
            
            if time.time() - self.competition_start_time >= 15 and self.competition_state == 'autonomous':
                self.competition_state = 'driver'; self._attributes['driver_control']['value'] = True; self._attributes['autonomous']['value'] = False
                self.competition_thread.stop()
                for x in range(5, 0, -1): print(f"[VexEmulator(CompetitionController)] driver control in {x}"); time.sleep(1)
                self.competition_thread = StoppableThread(self.user_control); self.competition_thread.start()
                self.competition_start_time = time.time()
            elif time.time() - self.competition_start_time >= 90 and self.competition_state == 'driver':
                self.competition_state = 'end'; self._attributes['driver_control']['value'] = False; self._attributes['autonomous']['value'] = False
                self.competition_thread.stop()
    
    def StartCompetition(self):
        threading.Thread(target=self._CompetitionLoop).start()

    def CompetitionUserFunc(self, user_control, autonomous):
        print("[VexEmulator(CompetitionController)] Got user and autonomous functions")
        self.user_control, self.autonomous = user_control, autonomous

new_globals = {}
