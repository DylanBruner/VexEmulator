import pygame, time, math
import win32api, win32con, win32gui, threading

pygame.init()

def RemoveColorRange(image: pygame.Surface, startRange: int, stopRange: int):
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            if image.get_at((x, y))[0] >= startRange and image.get_at((x, y))[1] >= startRange and image.get_at((x, y))[2] >= startRange and image.get_at((x, y))[0] <= stopRange and image.get_at((x, y))[1] <= stopRange and image.get_at((x, y))[2] <= stopRange:
                image.set_at((x, y), (255, 0, 128))
    return image

def CheckCollision(rect: pygame.Rect):
    return rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

class BrainScreen(object):
    def __init__(self, size: tuple, location: tuple):
        self.size     = size
        self.location = location

        self.frame = pygame.Surface(size)
        self.frame.fill((0, 0, 0))

        self.yOffsetPixels = 33

        self.programName = 'Placeholder-Name'

        self.maxRows = 12
        self.maxCols = 8

        self.startTime = time.time()

        self.penColor  = (255, 255, 255)
        self.penWidth  = 1
        self.fillColor = (255, 255, 255)
        self.cRow = 0
        self.cCol = 0
        self.x = 0
        self.y = 0

        self._clickEventCallbacks   = []
        self.font = pygame.font.SysFont("monospace", 20)

    def set_pen_color(self, color: tuple): self.penColor = color
    def draw_pixel(self, x, y): self.frame.set_at((x, y + self.yOffsetPixels), self.penColor)
    def clear_row(self, row): self.frame.fill((0, 0, 0), (0, row * self.size[1] / self.maxRows, (self.size[0], self.size[1] / self.maxRows) + self.yOffsetPixels))
    def clear_screen(self): self.frame.fill((0, 0, 0)); self.cCol = 0; self.cRow = 0
    def column(self): return self.col
    def row(self): return self.cRow
    def draw_circle(self, x, y, radius): pygame.draw.circle(self.frame, self.fillColor, (x, y + self.yOffsetPixels), radius, self.penWidth)
    def draw_line(self, start_x, start_y, stop_x, stop_y): pygame.draw.line(self.frame, self.fillColor, (start_x, start_y + self.yOffsetPixels), (stop_x, stop_y + self.yOffsetPixels), self.penWidth)
    def draw_rectangle(self, x, y, width, height): 
        pygame.draw.rect(self.frame, self.fillColor, (x, y + self.yOffsetPixels, width, height))
        pygame.draw.rect(self.frame, self.penColor, (x, y + self.yOffsetPixels, width, height), width = self.penWidth)

    def next_row(self): self.cRow += 1; self.cCol = 0
    def pressed(self, callback: callable): self._clickEventCallbacks.append(callback)
    def pressing(self) -> bool: return pygame.mouse.get_pressed()[0] and self.frame.get_rect().collidepoint(pygame.mouse.get_pos())
    def print(self, *args):
        text = ""
        for arg in args:
            text += str(arg) + " "            
        text = self.font.render(text, True, (255, 255, 255))
        self.frame.blit(text, ((self.cCol * self.size[0] / self.maxCols), (self.cRow * self.size[1] / self.maxRows)+self.yOffsetPixels))
        self.cCol += 1
        if self.cCol >= self.maxCols:
            self.cCol = 0
            self.cRow += 1
            if self.cRow >= self.maxRows:
                self.cRow = 0
                self.clear_row(0)
                self.cRow = 1
                self.cCol = 0
    def set_cursor(self, row, column): self.cRow = row; self.cCol = column
    def set_fill_color(self, color: tuple): self.fillColor = color
    def x_position(self): return self.x
    def y_position(self): return self.y  + self.yOffsetPixels
    def set_pen_width(self, width: int): self.penWidth = width
    
    def _draw(self, window: pygame.Surface):
        if pygame.mouse.get_pressed()[0] and self.frame.get_rect().collidepoint(pygame.mouse.get_pos()):
            for event_callback in self._clickEventCallbacks:
                event_callback()
        
        pygame.draw.rect(self.frame, (0, 153, 203), (0, 0, 480, 33))
        #Draw the program name on the left
        text = self.font.render(self.programName, True, (255, 255, 255))
        self.frame.blit(text, (0, 0))
        #Display the time sience the program started in the middle of the top bar
        text = self.font.render(time.strftime("%M:%S", time.gmtime(time.time() - self.startTime)), True, (255, 255, 255))
        self.frame.blit(text, (self.size[0] / 2, 0))

        window.blit(self.frame, self.location)

class Brain(object):
    def __init__(self):
        self.window = pygame.display.set_mode((674, 466), pygame.NOFRAME)

        self.BrainFrameImage = pygame.image.load("data/images/brainoutline.png")
        self.BrainFrameImage = self.BrainFrameImage.convert_alpha()
        self.BrainFrameImage = RemoveColorRange(self.BrainFrameImage, 235, 255)

        self.TransparentColor = (255, 0, 128)

        self.usedPorts = []

        self.BrainScreenSize = (480, 272)
        self.BrainScreen     = BrainScreen(self.BrainScreenSize, (68, 110))

        self.hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)

        self.makingSelection = False
        self.selectionStart  = None
        self.selectionStop   = None

        self.powerButtonRect = pygame.Rect((582, 217), (60, 60))
        self.topBar = pygame.Rect((10, 0), (648, 60))

    def tickmainloop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if CheckCollision(self.powerButtonRect):
            pygame.quit(); quit()
        elif CheckCollision(self.topBar):
            #Allow the window to be dragged
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], 0, 0, win32con.SWP_NOSIZE)
        
        self.window.fill((255, 0, 128))
        
        self.window.blit(self.BrainFrameImage, (0, 0))

        self.BrainScreen._draw(self.window)

        pygame.display.update()

class Timer(object):
    def __init__(self):
        self._start_time = time.time()
        self._callbacks  = []

        threading.Thread(target=self._callback_manager).start()

    def _callback_manager(self):
        while True:
            time.sleep(0.1)
            for callback in self._callbacks:
                if callback[0] == math.floor(time.time() - self._start_time):
                    callback[1]()
                    self._callbacks.remove(callback)
    
    def clear(self): self._start_time = time.time()
    def time(self, units): 
        if units == 'msec': return time.time() - self._start_time * 1000
        return time.time() - self._start_time

    def event(self, callback: callable, time: float): self._callbacks.append((time, callback))

class Battery(object):
    def __init__(self):
        self._capacity = 85
        self._current  = 15
        self._voltage  = 12.6 
    
    def capacity(self): return self._capacity
    def current(self, units):  return self._current
    def voltage(self, units):  return self._voltage

class BrainLinker(object):
    def __init__(self, screen: BrainScreen, battery: Battery, timer: Timer):
        self.screen  = screen
        self.battery = battery
        self.timer   = timer