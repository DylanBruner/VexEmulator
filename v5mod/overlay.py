import pyautogui, v5mod.pygameoverlay as pygameoverlay, pygame
from win32gui import GetWindowText, GetForegroundWindow
from PIL import Image
import easyocr

def getActiveWindow() -> str: return GetWindowText(GetForegroundWindow())
def findButton(image): return pyautogui.locateOnScreen(image, confidence=.8)

class VexCodeOverlay(object):
    def __init__(self):
        self.overlayImage = pygame.image.load('data/images/runoverlay.png')
        self.Overlay = pygameoverlay.NewOverlay((27, 45), (0, 0))
        self.Overlay.window.blit(self.overlayImage, (0, 0))

        self.pressed = False

        self.LastWindowLocation    = (0, 0)
        self.CurrentButtonLocation = (0, 0)
    
    def _extractTextFromScreenshot(self):
        reader = easyocr.Reader(['en'])
        output = reader.readtext('data/temp/screenshot.png')
        return output[0][1]

    def getProjectName(self):
        if loc := pyautogui.locateOnScreen('data/images/savedtext.png', confidence=0.9):
            pyautogui.screenshot('data/temp/screenshot.png', region=(loc[0]-150, loc[1], 145, 40))
            return self._extractTextFromScreenshot()


    def tick(self):
        if getActiveWindow() in ['VEXcode V5', 'pygame window']:
            self.Overlay.window.blit(self.overlayImage, (0, 0))
            self.pressed = self.Overlay.clicked(self.CurrentButtonLocation)
            
            if button := findButton('data/images/runbutton.png'):
                self.CurrentButtonLocation = button[0], button[1]
                self.Overlay.goto((button[0], button[1]))
            elif not findButton('data/images/rundetect.png'):
                print('Button should be here, but it\'s not.')
        
        else:
            self.Overlay.hide()
        
        self.Overlay.tick()