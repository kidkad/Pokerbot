import os

class parser:
    """
    Parser parses through the debug.txt file present in the Pokermuck folder.
    This text file is updated in realtime based on the image recognition of the
    HUD.
    When PokerMuck is installed, it dynamically generates an installation
    location (I don't know why). The find_file method will return the folder
    where "debug.txt" is located.
    """

    #filepath = path to debut.txt
    def __init__(self, filepath):
        self.file = filepath

    #return folder containing PokerMuck.exe and debug.txt
    def find_file(self):
        for root, dirs, files in os.walk('C:\\Users\\Brunope\\AppData\\Local\\Apps\\2.0\\'):
            if 'PokerMuck.exe' in files:
                self.file = os.path.join(root, 'debug.txt')
                return self.file

    def print_filepath(self):
        print self.file
        print list(open(self.file, 'r'))

    #returns the current hand number
    #will not support multitabling
    def get_hand_number(self):
        try:
            myfile = open(self.file, 'r')
            line_list = list(myfile)
            #iterate from bottom of file, looking for hand number
            for i in range(len(line_list)-1, 0, -1):
                if line_list[i][:13] == "Starting hand":
                    #parse hand number
                    hand = line_list[i][15:].strip()
                    return hand
        finally:
            myfile.close()

    #return most recent hole cards
    def get_hole_cards(self):
        try:
            myfile = open(self.file, 'r')
            line_list = list(myfile)
            for i in range(len(line_list)-1, 0, -1):
                if line_list[i][:20].lower() == "matched player cards":
                    return line_list[i][22:].strip().split()
        finally:
            myfile.close()

    def get_board_cards(self):
        try:
            myfile = open(self.file, 'r')
            line_list = list(myfile)
            for i in range(len(line_list)-1, 0, -1):
                if line_list[i][:19].lower() == "matched board cards":
                    return line_list[i][21:].strip().split()
        finally:
            myfile.close()

    #return hero's name
    def get_hero_name(self):
        try:
            myfile = open(self.file, 'r')
            line_list = list(myfile)
            for i in range(len(line_list)-1, 0, -1):
                if line_list[i][:17].lower() == "found hero's name":
                    return line_list[i][19:].strip()
        finally:
            myfile.close()

    def get_stack_at_round_start(self):
        pass

if __name__ == "__main__":
    myparser = parser('')
    myparser.find_file()
    print myparser.get_hole_cards()