import pygame, time

def SimpleAlert(brain, text: list or str):
    if type(text) == list: return Popup(brain, text, ['ok'], lambda x: None)
    else: return Popup(brain, [text], ['ok'], lambda x: None)

class Popup(object):
    def __init__(self, brain, text: list, options: list, callback: callable):
        self.brain       = brain
        self.window      = brain.overlayFrame
        self.window_size = self.window.get_size()

        self.originalFontSize = 20
        self.currentFontSize  = 20
        self.font       = pygame.font.SysFont('monospace', self.currentFontSize)
        self.buttonFont = pygame.font.SysFont('monospace', 18)
        self.textLines  = text
        self.options  = options
        self.callback = callback

        self.buttonIdle  = (57, 57, 60)
        self.buttonHover = (42, 42, 44)

        self.finished = False

        self.buttonCooldown = 200

        #Get longest option
        self.popup = pygame.Surface((400, 250), pygame.SRCALPHA)
        self.buttonWidth = self.buttonFont.size(max(options, key=len))[0] + 20

        self.brain.BrainScreen.inputFrozen = True
    
    def destroy_popup(self):
        self.brain.overlayFrame.fill((255, 255, 255, 0))
        self.popup.fill((255, 255, 255, 0))
        self.brain.BrainScreen.inputFrozen = False
        self.finished = True
    
    def get_relative_mouse_pos(self):
        Location = pygame.mouse.get_pos()[0] - 111, pygame.mouse.get_pos()[1] - 122
        if Location[0] < 0: Location = 0, Location[1]
        if Location[1] < 0: Location = Location[0], 0
        if Location[0] > self.popup.get_width(): Location = self.popup.get_width(), Location[1]
        if Location[1] > self.popup.get_height(): Location = Location[0], self.popup.get_height()
        return Location
 
    def draw_buttons(self):
        for option in self.options:
            buttonLocation = ((self.popup.get_width() // 2) - (self.buttonWidth // 2), 
                             (self.options.index(option) * 25) + (self.popup.get_height() // 2))

            rect = pygame.Rect((buttonLocation[0], buttonLocation[1], self.buttonWidth, 20))
            rectColor = self.buttonIdle

            if rect.collidepoint(self.get_relative_mouse_pos()):
                if pygame.mouse.get_pressed()[0] and self.buttonCooldown <= 0:
                    self.destroy_popup()
                    self.callback(option)
                    time.sleep(.15)
                    return
                else:
                    rectColor = self.buttonHover

            pygame.draw.rect(self.popup, rectColor, rect, border_radius=5)
            text = self.buttonFont.render(option, True, (255, 255, 255))
            self.popup.blit(text, (buttonLocation[0] + (self.buttonWidth // 2) - (text.get_width() // 2), buttonLocation[1] + (20 // 2) - (text.get_height() // 2)))

    def tick(self):
        if self.finished: return

        self.buttonCooldown -= 1

        #Blit self.popup into the middle of self.window
        self.popup.fill((19, 20, 23))
        #Draw self.text into the the middle of self.popup 1/3 of the way down
        #in the middle

        for line in self.textLines:
            while self.font.size(line)[0] > self.popup.get_width():
                self.currentFontSize -= 1
                self.font = pygame.font.SysFont('monospace', self.currentFontSize)

            text = self.font.render(line, True, (255, 255, 255))
            self.popup.blit(text, (self.popup.get_width() // 2 - text.get_width() // 2, 10 + (self.textLines.index(line) * 20)))
            self.font = pygame.font.SysFont('monospace', self.originalFontSize); self.currentFontSize = self.originalFontSize

        self.draw_buttons()

        self.brain.overlayFrame.fill((255, 255, 255, 0))
        self.brain.overlayFrame.blit(self.popup, ((self.window_size[0] // 2 - self.popup.get_size()[0] // 2)-26, 
                                                 (self.window_size[1] // 2 - self.popup.get_size()[1] // 2)+15))