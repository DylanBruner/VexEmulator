class Bumper(object):
    def __init__(self):
        self._pressed = False
        self._pressCallbacks   = []
        self._reelaseCallbacks = []
    
    def pressing(self) -> bool: return self._pressed
    def pressed(self, callback: callable): self._pressCallbacks.append(callback)
    def released(self, callback: callable): self._reelaseCallbacks.append(callback) 