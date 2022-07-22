import pygame, time, math, pygamepopup, json
import win32api, win32con, win32gui, threading, os
from PIL import Image

TransparentColor = (255, 0, 128)

pygame.init()

def RemoveColorRange(image: pygame.Surface, startRange: int, stopRange: int, keyColor=(255, 0, 128)):
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            if image.get_at((x, y))[0] >= startRange and image.get_at((x, y))[1] >= startRange and image.get_at((x, y))[2] >= startRange and image.get_at((x, y))[0] <= stopRange and image.get_at((x, y))[1] <= stopRange and image.get_at((x, y))[2] <= stopRange:
                image.set_at((x, y), keyColor)
    return image

def CheckCollision(rect: pygame.Rect):
    return rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

class BrainScreen(object):
    def __init__(self, size: tuple, location: tuple):
        self.size     = size
        self.location = location

        self._attributes = {}

        self.inputFrozen = False

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

        self.mouseDown = False

        self._drawProgramBar = False

        self._clickEventCallbacks   = []
        self._releaseEventCallbacks = []
        self.font = pygame.font.SysFont("monospace", 20)
    
    def _getRelativeMouseLocation(self) -> tuple:
        if self.inputFrozen: return (0, 0)
        return (pygame.mouse.get_pos()[0] - 69, pygame.mouse.get_pos()[1] - 110)

    def set_pen_color(self, color: tuple): self.penColor = color
    def draw_pixel(self, x, y): self.frame.set_at((x, y + self.yOffsetPixels), self.penColor)
    def clear_row(self, row):
        rowRect = pygame.Rect(0, ((row - 1)* self.size[1] / self.maxRows) + self.yOffsetPixels, self.size[0], self.size[1] / self.maxRows)
        self.frame.fill((0, 0, 0), rowRect)
    
    def clear_screen(self): self.frame.fill((0, 0, 0)); self.cCol = 0; self.cRow = 0
    def column(self): return self.col
    def row(self): return self.cRow
    def draw_circle(self, x, y, radius): pygame.draw.circle(self.frame, self.fillColor, (x, y + self.yOffsetPixels), radius, self.penWidth)
    def draw_line(self, start_x, start_y, stop_x, stop_y): pygame.draw.line(self.frame, self.fillColor, (start_x, start_y + self.yOffsetPixels), (stop_x, stop_y + self.yOffsetPixels), self.penWidth)
    def draw_rectangle(self, x, y, width, height, color = None):
        if color is None: color = self.fillColor
        pygame.draw.rect(self.frame, color, (x, y + self.yOffsetPixels, width, height))
        pygame.draw.rect(self.frame, self.penColor, (x, y + self.yOffsetPixels, width, height), width = self.penWidth)

    def next_row(self): self.cRow += 1; self.cCol = 0
    def pressed(self, callback: callable): self._clickEventCallbacks.append(callback)
    def release(self, callback: callable): self._releaseEventCallbacks.append(callback)
    def pressing(self) -> bool: return self.mouseDown
    def print(self, *args):
        # sourcery skip: use-fstring-for-concatenation, use-join
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

    def set_cursor(self, row, column): self.cRow = row - 1; self.cCol = column - 1
    def set_fill_color(self, color: tuple): self.fillColor = color
    def x_position(self): return self.x
    def y_position(self): return self.y
    def set_pen_width(self, width: int): self.penWidth = width
    
    def _draw(self, window: pygame.Surface):
        #Mouse events
        checks = (
            self._getRelativeMouseLocation()[0] <= self.size[0],
            self._getRelativeMouseLocation()[0] >= 0,
            self._getRelativeMouseLocation()[1] <= self.size[1],
            self._getRelativeMouseLocation()[1] >= 0,
            pygame.mouse.get_pressed()[0]
        )

        if all(checks) and not self.mouseDown:
            self.mouseDown = True
            self.x, self.y = self._getRelativeMouseLocation()
            for event_callback in self._clickEventCallbacks:
                event_callback()
        elif not all(checks) and self.mouseDown:
            self.mouseDown = False
            for event_callback in self._releaseEventCallbacks:
                event_callback()

        
        if self._drawProgramBar:
            pygame.draw.rect(self.frame, (0, 153, 203), (0, 0, 480, 33))
            text = self.font.render(self.programName, True, (255, 255, 255))
            self.frame.blit(text, (0, 0))
            text = self.font.render(time.strftime("%M:%S", time.gmtime(time.time() - self.startTime)), True, (255, 255, 255))
            self.frame.blit(text, (self.size[0] / 2, 0))

        window.blit(self.frame, self.location)

class Brain(object):
    def __init__(self):
        #This 70 line init really needs to be cleaned up
        self.window = pygame.display.set_mode((674, 466), pygame.NOFRAME)
        self.BrainScreenSize = (480, 272)

        self.overlayFrame    = pygame.Surface((674, 466), pygame.SRCALPHA)

        self.BrainFrameImage = pygame.image.load("data/images/brainoutline.png")
        self.BrainFrameImage = self.BrainFrameImage.convert_alpha()
        self.BrainFrameImage = RemoveColorRange(self.BrainFrameImage, 235, 255)

        self.BrainHomeImage  = pygame.image.load("data/images/brainhomescreen.png")
        self.BrainHomeImage  = self.BrainHomeImage.convert_alpha()
        self.BrainHomeImage  = RemoveColorRange(self.BrainHomeImage, 254, 255)#Remove the little white vert line on the far right
        self.BrainHomeImage  = pygame.transform.scale(self.BrainHomeImage, (self.BrainScreenSize[0] + 1, self.BrainScreenSize[1]))#Cover the white vert line thats now gone

        self.BrainProgramImage = pygame.image.load("data/images/programlogo.png")
        self.BrainProgramImage = self.BrainProgramImage.convert_alpha()
        self.BrainProgramImage = RemoveColorRange(self.BrainProgramImage, 250, 255)
        #Scale it to be 40%
        self.ProgramIconSmall = pygame.image.load('data/images/programlogo.png')
        self.ProgramIconSmall = self.ProgramIconSmall.convert_alpha()
        self.ProgramIconSmall = RemoveColorRange(self.ProgramIconSmall, 250, 255)
        self.ProgramIconSmall = pygame.transform.scale(self.ProgramIconSmall, (51, 51))

        self.BrainProgramImage = pygame.transform.scale(self.BrainProgramImage, (int(self.BrainProgramImage.get_width() * 0.30), int(self.BrainProgramImage.get_height() * 0.30)))

        self.BrainDeviceScreen = pygame.image.load('data/images/deviceinfoscreen.png')
        self.BrainDeviceScreen = pygame.transform.scale(self.BrainDeviceScreen, (int(self.BrainDeviceScreen.get_width() * 1.62), 
                                                                                 int(self.BrainDeviceScreen.get_height() * 1.6)))

        self.BrainUserFolderScreen = pygame.image.load('data/images/userfolder.png')
        self.BrainUserFolderScreen = pygame.transform.scale(self.BrainUserFolderScreen, (int(self.BrainUserFolderScreen.get_width() * 1.62), 
                                                                                         int(self.BrainUserFolderScreen.get_height() * 1.6)))
        self.EmptyProgramIcon = pygame.image.load('data/images/programslot.png')

        self.ProgramButtonSize = self.BrainProgramImage.get_size()
        self.ProgramLocations  = [(25, 170), (150, 170), (265, 170)]
        self.ProgramsLoaded    = []

        self.TransparentColor = (255, 0, 128)

        self.usedPorts      = []
        self.virtualDevices = []

        self.BrainScreen     = BrainScreen(self.BrainScreenSize, (68, 110))

        self.hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)

        self.makingSelection  = False
        self.selectionStart   = None
        self.selectionStop    = None
        self.canMakeSelection = False

        self.onHomeScreen          = True
        self.onDeviceScreen        = False
        self.onProgramScreen       = False
        self.onProgramFolderScreen = False

        self.powerButtonRect = pygame.Rect((582, 217), (60, 60))
        self.topBar = pygame.Rect((10, 0), (648, 60))

        self.font = pygame.font.SysFont("monospace", 12)

        self.DeviceInfoButton    = pygame.Rect((129, 43),  (100, 100))
        self.UserProgramsButton  = pygame.Rect((375, 167), (100, 100))

        self.buttonCooldown = 5000
        self.popups         = []

        self.legacyMode     = False
        self.CodeEnviorment = None
    
    def takeScreenshot(self):
        pygame.image.save(self.BrainScreen.frame, f'data/screenshots/{time.strftime("ScreenShot_%H.%M.%S.png", time.gmtime())}')
    
    def legacyModePrompt(self, clicked: str):
        if clicked.lower().strip() == "yes":
            self.legacyMode = True
            print("[VexEmulator(Brain)] Legacy mode enabled")
        elif clicked.lower().strip() == "no":
            self.legacyMode = False
            print("[VexEmulator(Brain)] Legacy mode disabled")
        elif clicked.lower().strip() == "don't ask again":
            with open('data/config.json') as f: data = json.load(f)
            data['promptLegacyMode'] = False
            with open('data/config.json', 'w') as f: json.dump(data, f)
            print("[VexEmulator(Brain)] Legacy mode prompt disabled")

    def runHomeScreen(self):
        self.BrainScreen.frame.blit(self.BrainHomeImage, (0, 0))#Draw the home screen

        if self.DeviceInfoButton.collidepoint(self.BrainScreen._getRelativeMouseLocation()) and pygame.mouse.get_pressed()[0]:
            self.onHomeScreen   = False
            self.onDeviceScreen = True
        elif self.UserProgramsButton.collidepoint(self.BrainScreen._getRelativeMouseLocation()) and pygame.mouse.get_pressed()[0]:
            self.onHomeScreen          = False
            self.onProgramFolderScreen = True

        #Draw the program selector buttons
        for location, program in zip(self.ProgramLocations, self.ProgramsLoaded):
            self.BrainScreen.frame.blit(self.BrainProgramImage, location)
            #Draw program.name under the logo
            if len(program.name) > 10: text = self.font.render(f'{program.name[:10]}...', True, (255, 255, 255))
            else: text = self.font.render(program.name, True, (255, 255, 255))

            self.BrainScreen.frame.blit(text, (location[0], location[1]+self.BrainProgramImage.get_height()+5))

            if pygame.Rect(location[0], location[1], self.ProgramButtonSize[0], self.ProgramButtonSize[1]).collidepoint(self.BrainScreen._getRelativeMouseLocation()) and pygame.mouse.get_pressed()[0]:
                self.onHomeScreen = False
                self.BrainScreen._drawProgramBar = True
                self.BrainScreen.clear_screen()
                self.onProgramScreen = True
                program.reloadContainerCode()
                self.CodeEnviorment  = program.loadContainer(self)
                self.CodeEnviorment.threadedExecute()

    def runDeviceScreen(self):
        self.BrainScreen.frame.blit(self.BrainDeviceScreen, (0, 0))
    
    def runUserProgramScreen(self):
        self.BrainScreen.frame.blit(self.BrainUserFolderScreen, (0, 0))
        #Create the empty program buttons
        ButtonsPerRow = self.BrainScreen.size[0] // (self.EmptyProgramIcon.get_width() + 35)
        AmountOFRows  = 3

        for row in range(AmountOFRows):
            for button in range(ButtonsPerRow):
                self.BrainScreen.frame.blit(self.EmptyProgramIcon, ((button * (self.EmptyProgramIcon.get_width() + 35)) + 20, 
                                                                    (row * (self.EmptyProgramIcon.get_height() + 35)) + self.BrainScreen.yOffsetPixels + 20))

        CurrentButton = 0
        CurrentRow    = 0

        for program in self.ProgramsLoaded:
            location = ((CurrentButton * (self.EmptyProgramIcon.get_width() + 35)) + 20, 
                        (CurrentRow * (self.EmptyProgramIcon.get_height() + 35)) + self.BrainScreen.yOffsetPixels + 20)
            #Draw a self.ProgramImage under the button
            self.BrainScreen.frame.blit(self.ProgramIconSmall, location)
            #Draw program.name under the logo
            if len(program.name) > 10: text = self.font.render(f'{program.name[:10]}...', True, (255, 255, 255))
            else: text = self.font.render(program.name, True, (255, 255, 255))
            self.BrainScreen.frame.blit(text, (location[0], location[1]+55))

            if CurrentButton > ButtonsPerRow - 2:
                CurrentRow += 1
                CurrentButton = 0
            else:
                CurrentButton += 1
            Rect = pygame.Rect(location[0], location[1], 51, 51)
            if Rect.collidepoint(self.BrainScreen._getRelativeMouseLocation()) and pygame.mouse.get_pressed()[0]:
                self.onProgramFolderScreen       = False
                self.BrainScreen._drawProgramBar = True
                self.BrainScreen.clear_screen()
                self.onProgramScreen = True
                self.CodeEnviorment  = program.loadContainer(self)
                self.CodeEnviorment.threadedExecute()
        
    
    def selectionTick(self):
            if pygame.mouse.get_pressed()[0] and not self.makingSelection:
                self.makingSelection = True
                self.selectionStart = self.BrainScreen._getRelativeMouseLocation()
            elif self.makingSelection and not pygame.mouse.get_pressed()[0]:
                self.makingSelection = False
                self.selectionStop = self.BrainScreen._getRelativeMouseLocation()
                self.BrainScreen.clear_screen()
                #Make a rect out of self.selectionStart and self.selectionStop
                selectionRect = pygame.Rect(self.selectionStart, self.selectionStop)
                print(f"Selection start: {self.selectionStart}, {selectionRect.width}x{selectionRect.height}")
            elif self.makingSelection:
                #Draw a box from self.selectionStart to self.BrainScreen._getRelativeMouseLocation()
                self.BrainScreen.frame.fill((0, 0, 0), pygame.Rect(self.selectionStart[0], self.selectionStart[1], self.BrainScreen._getRelativeMouseLocation()[0] - self.selectionStart[0], self.BrainScreen._getRelativeMouseLocation()[1] - self.selectionStart[1]))

    def teardownProgram(self):
        self.CodeEnviorment.stop()
        self.BrainScreen.clear_screen()

        #Reset the screen
        self.BrainScreen = BrainScreen(self.BrainScreen.size, self.BrainScreen.location)

    def tickmainloop(self):
        self.buttonCooldown -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.takeScreenshot()
                    print("[VexEmulator(Brain)] Screenshot taken")

        if CheckCollision(self.powerButtonRect) and self.buttonCooldown <= 0:
            self.buttonCooldown = 180
            if self.onHomeScreen: pygame.quit(); quit()
            elif self.onDeviceScreen: self.onHomeScreen        = True; self.onDeviceScreen        = False
            elif self.onProgramFolderScreen: self.onHomeScreen = True; self.onProgramFolderScreen = False
            elif self.onProgramScreen: 
                self.onHomeScreen = True; self.onProgramScreen = False; self.BrainScreen._drawProgramBar = False
                print('[VexEmulator(Brain)] Attempting to teardown container...')
                self.teardownProgram()
                print('[VexEmulator(Brain)] Container teardown complete!')
        elif CheckCollision(self.topBar):
            #Allow the window to be dragged
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], 0, 0, win32con.SWP_NOSIZE)

        self.window.fill((255, 0, 128))

        self.window.blit(self.BrainFrameImage, (0, 0))
        if self.onHomeScreen: self.runHomeScreen()
        elif self.onDeviceScreen: self.runDeviceScreen()
        elif self.onProgramFolderScreen: self.runUserProgramScreen()
        
        #Draw a selection box if the mouse is pressed
        if self.canMakeSelection: self.selectionTick()

        if self.onProgramScreen and self.CodeEnviorment is not None:
            if self.CodeEnviorment.executionFailed:
                self.onProgramScreen = False; self.onHomeScreen = True; self.BrainScreen._drawProgramBar = False
                self.teardownProgram()
                with open('data/config.json') as f:
                    if json.load(f)['promptLegacyMode'] and not self.legacyMode:
                        self.popups.append(pygamepopup.Popup(self, ['Code failed!','Enable legacy support?','',str(self.CodeEnviorment.executionFailureReason)], 
                                                                   ['Yes','No',"Don't ask again"], self.legacyModePrompt))
                    else:
                        self.popups.append(pygamepopup.SimpleAlert(self, ['Code failed!',f'Legacy Mode: {self.legacyMode}','',str(self.CodeEnviorment.executionFailureReason)]))

        for popup in self.popups: popup.tick()

        self.BrainScreen._draw(self.window)
        self.window.blit(self.overlayFrame, (0, 0))
        
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
        self._attributes = {
            'capacity': {'type': 'int', 'value': 85},
            'current':  {'type': 'int', 'value': 15},
            'voltage':  {'type': 'float', 'value': 12.6}
        }
    
    def capacity(self): return self._attributes['capacity']['value']
    def current(self, units):  return self._attributes['current']['value']
    def voltage(self, units):  return self._attributes['voltage']['value']

class BrainLinker(object):
    def __init__(self, screen: BrainScreen, battery: Battery, timer: Timer):
        self.screen  = screen
        self.battery = battery
        self.timer   = timer