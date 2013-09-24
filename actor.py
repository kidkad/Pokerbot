import win32api
import win32con
import random
import win32gui
import time
import ImageEnhance
import ImageOps
from pytesser import *
from PIL import ImageGrab
import AI

class Actor:
    """
    The Actor class provides methods for interacting with the game window itself.
    It requires the window to be in the upper left corner of the screen. Methods
    that emulate mouse clicks click randomly within the button's borders as a
    measure against bot detection.
    """

    global enum_cb, move_window, get_pixelsixels

    def __init__(self):
        global toplist, winlist
        toplist, winlist = [], []

    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    def move_window(hwnd, x, y, width, height):
        box = win32gui.GetWindowRect(hwnd)
        #move window to (x, y) and change size to (width x height)
        win32gui.MoveWindow(hwnd, x, y, width, height, False)

    def get_pixels(self, hwnd):
        color = win32gui.GetPixel(win32gui.GetDC(hwnd), 100, 100)
        print color

    def is_turn(self):
        win32gui.EnumWindows(enum_cb, toplist)
        window = [(hwnd, title) for hwnd, title in winlist if "(0+0)" in title.lower()]
        #store PyHANDLE object
        try:
            window = window[0]
            hwnd = window[0]
        except IndexError:
            print "Table window not found."
        #print "Found window! " + win32gui.GetWindowText(hwnd)

        box = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(box)
        R,G,B = img.getpixel((459, 535))
        #R, G, and B are 182 when action buttons appear
        if R == 182 and G == 182 and B == 182:
            return True

    def get_blinds(self):
        box = (39, 522, 288, 552)
        time.sleep(2)
        img = ImageGrab.grab(box)
        img = img.convert('L')
        enh = ImageEnhance.Contrast(img)
        img = enh.enhance(2)
        img = ImageOps.invert(img)
        img.show()

        print image_to_string(img)
        #im = Image.open("blinds.tif")

    def get_stack(self):
        box = (490, 428, 570, 440)
        time.sleep(2)
        img = ImageGrab.grab(box)
        #img = ImageOps.invert(img)
        img = img.convert('L')
        enh = ImageEnhance.Contrast(img)
        img = enh.enhance(1.5)
        #img = ImageOps.invert(img)
        #img = img.convert('1')
        img = img.resize((800, 120))
        img.show()
        print image_to_string(img)

    def fold(self):
        xpos = random.randint(342, 434)
        ypos = random.randint(530, 548)
        win32api.SetCursorPos((xpos, ypos))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        return 0

    #click random position within "call" button
    def call(self):
        xpos = random.randint(456, 564)
        ypos = random.randint(530, 548)
        win32api.SetCursorPos((xpos, ypos))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        return 0

    #raise to 'amount'
    def raise_to(self, amount):
        xpos = random.randint(586, 692)
        ypos = random.randint(530, 548)
        win32api.SetCursorPos((xpos, ypos))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        return 0

    #push all in
    def shove(self):
        xpos = 567
        ypos = 488
        win32api.SetCursorPos((xpos, ypos))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        xpos = 700
        ypos = 482
        win32api.SetCursorPos((xpos, ypos))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        xpos= random.randint(580, 680)
        ypos = random.randint(530, 548)
        win32api.SetCursorPos((xpos, ypos))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        return 0


if __name__ == "__main__":
    actor = Actor()
    actor.get_stack()
    #time.sleep(2)
    #actor.shove()
