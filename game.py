import debug_parser
import time

class Gamestate:
    """
    Gamestate represents the current state of the game, storing all information,
    such as previous action in a round, players in the hand, blinds, antes, hole
    cards, and board cards.
    """

    def __init__(self):
        self.sblind = 0
        self.bblind = 0
        self.ante = 0
        self.pot = 0
        self.side_pot = 0
        self.player_names = []
        self.player_objects = []
        self.actions = []
        self.hole = []
        self.board = []
        self.start_level = time.time()
        self.level = 0 #blind level starts at 0 for 30 prize, 1 for 3 prize
        #set blind levels
        self.blinds = ["10/200:0",
                       "15/30:0",
                       "25/50:0",
                       "50/100:0",
                       "75/150:0",
                       "100/200:0",
                       "100/200:25",
                       "200/400:25",
                       "300/600:50",
                       "400/800:50",
                       "600/1200:75",
                       "800/1600:75",
                       "1000/2000:100",
                       "1500/3000:150",
                       "2000/4000:200",
                       "3000/6000:300",
                       "4000/8000:400"]

    #Get all information using debug_parser and store it.
    def update(self):
        #self.board = debug_parser.parser().get_board_cards()
        #self.hole = debug_parser.parser().get_hole_cards()
        if time.time() - self.start_level >= 14400:
            #has been more than 4 minutes
            self.level += 1
        blinds = self.blinds[self.level]
        self.sblind = blinds[:blinds.find("/")]
        self.bblind = blinds[blinds.find("/")+1:blinds.find(":")]
        self.ante = blinds[blinds.find(":")+1:]



class Player:
    """
    Player stores all information about a current player (table position,
    relative position, stack size). It also writes statistics about the player
    to a file(# of hands played, # of times gone to showdown, VPIP, fold blind
    to PFR, Cbet %, 3bet %, 4bet %, push %, bluff %, and type). Type is stored
    as a string, i.e. 'loose aggressive', 'tight passive', etc.
    """

    def __init__(self):
        self.filepath = '' #path to file containing player statistics.
        self.table_pos = 0
        self.relative_pos = 0
        self.stack = 0
        self.num_hands = 0
        self.num_showdowns = 0
        self.VPIP = 0
        self.type = ''
        self.cbet_freq = 0
        self.PFR_freq = 0
        self.three_bet_freq = 0
        self.four_bet_freq = 0
        self.push_freq = 0
        self.fold_to_PFR_freq = 0
        self.bluff_freq = 0

    #After each round, update player with gamestate info.
    def update(self, state):
        pass