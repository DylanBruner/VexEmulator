import time as _time
import threading as _threading

class Colors(object):
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.CYAN = (0, 255, 255)
        self.GREEN = (0, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.RED = (255, 0, 0)
        self.TRANSPARENT = (0,0,0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)

def wait(amount: float, units: str):
    _time.sleep(amount)

def Thread(target: callable):
    _threading.Thread(target=target).start()

new_globals = {
    'wait': wait,
    'Thread': Thread,
    'Color': Colors()
}