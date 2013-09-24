import os
import time
import win32gui
import sys
import check_turn
import actor
import AI
import debug_parser

class Bot:
    """This is the main class for BruBot."""

    def __init__(self):
        self.filepath = ""
        #find filepath and pass it to debug_parser
        for root, dirs, files in os.walk(r'C:\Users\Brunope\AppData\Local\Apps\2.0'):
            if 'PokerMujslkahdck.exe' in files:
                self.filepath = os.path.join(root)
        if self.filepath == "":
            #Pokermuck not installed
            print "Error: PokerMuck not installed. It must be actively running\
 for this bot to work."
            sys.exit()
        self.myparser = debug_parser.parser(self.filepath)
        self.turn_checker = check_turn.TurnChecker()
        self.AI = AI.AI()
        self.actor = actor.Actor()
        self.winlist = []
        self.toplist = []

    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    def prep_window(self):
        #move table window, and close other impeding windows
        #look for window
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        count = 0
        #close 9 HUD tracker windows that pop up
        while count <= 9:
            try:
                win32gui.EnumWindows(self.enum_cb, self.toplist)
                #print winlist
                for hwnd, title in winlist:
                    window = None
                    if "hudwindow" in title.lower():
                        window = [hwnd, title]
                        print hwnd
                        win32gui.DestroyWindow(hwnd)

                #window = [(hwnd, title) for hwnd, title in winlist if "hudwindow" in title.lower()]
                #win32gui.CloseWindow(hwnd)
                count += 1
            except:
                print "No HUDWindows"
                #No more HUDWindows
                break
        window = [(hwnd, title) for hwnd, title in self.winlist if "(0+0)" in title.lower()]
        #store PyHANDLE object
        try:
            window = window[0]
            hwnd = window[0]
        except IndexError:
            print "Table window not found."
            return
        #move window to foreground
        win32gui.SetActiveWindow(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        #get window size and position
        box = win32gui.GetWindowRect(hwnd)
        x = box[0]
        y = box[1]
        width = box[2] - x
        height = box[3] - y
        #move window to top left if not already there
        if x != 0 or y != 0:
            print "moving window"
            win32gui.MoveWindow(hwnd, x, y, width, height, False)
            x = 0
            y = 0


    def main(self):
        #continuously check for turn
        print"Prepping window"
        self.prep_window()
        while True:
            if self.actor.is_turn():
                print "Our turn to act!"
                self.myparser.find_file()
                print "Filepath to debug.txt: ", self.myparser.file
                #wait for pokermuck to write hole cards to file
                time.sleep(2)
                cards = self.myparser.get_hole_cards()
                print "Hole cards: ", cards
                print "Running hand strength sim..."
                action = self.AI.act(cards)
                print "Action decided: ", action
                amount = self.AI.raise_amount
                if action == "shove":
                    self.actor.shove()
                elif action == "fold":
                    self.actor.fold()
                elif action == "call":
                    self.actor.fold()
                elif action == "raise":
                    self.actor.raise_to(amount)
                else:
                    print action
            time.sleep(2)

if __name__ == "__main__":
    brubot = Bot()
    brubot.main()