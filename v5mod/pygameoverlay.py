import pygame
import win32api, win32con, win32gui

class NewOverlay(object):
    def __init__(self, size: tuple, location: tuple):
        self.transparent = (255, 0, 128)
        self.window = pygame.display.set_mode(size, pygame.NOFRAME)

        self.size =  size

        self.hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(*self.transparent), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, location[0], location[1], 0, 0, win32con.SWP_NOSIZE)

    def goto(self, location: tuple):
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, location[0], location[1], 0, 0, win32con.SWP_NOSIZE)

    def clicked(self, location: tuple) -> bool:
        return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) != 0 and pygame.Rect(location[0], location[1], self.size[0], self.size[1]).collidepoint(win32api.GetCursorPos())

    def hide(self):
        self.window.fill(self.transparent)

    def tick(self):
        for _ in pygame.event.get(): pass#Get events to make pygame happy
        pygame.display.update()