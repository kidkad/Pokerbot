import math
import itertools
import random
import actor
import game

class AI:

    global match_cards, bubble_sort, encode_card, encode_hand, shuffle_deck, hand_strength

    def __init__(self):
        self.Actor = actor.Actor()
        self.raise_amount = 0
        #list of player objects
        self.player_list = []
        self.hero = None

    #sorts a list using the bubble sort algorithm (bubble sort rocks!)
    def bubble_sort(mylist):
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(mylist) - 1):
                if mylist[i] > mylist[i+1]:
                    mylist[i], mylist[i+1] = mylist[i+1], mylist[i]
                    swapped = True
        return mylist

    def match_cards(card1, card2, match):
        hand = ""
        card1Num = card1[:1]
        card2Num = card2[:1]
        card1Suit = card1[1:2]
        card2Suit = card2[1:2]

        if card1Num == card2Num:
            hand = "%s%s" % (card1Num, card2Num)
        elif card1Suit == card2Suit:
            hand = "%s%ss" % (card1Num, card2Num)
        else:
            hand = "%s%so" % (card1Num, card2Num)
        if hand == match:
            return True
        else:
            return False

    #encode a card  as an integer equal to suit * 13 + rank
    #suit = card / 13, and rank = card % 13
    def encode_card(card):
        rank = card[:1]
        #convert rank to integer in range 0-12 (0 = 2, 1 = 3, ... A = 12, etc.)
        if rank == 'A':
            rank = 12
        elif rank == 'K':
            rank = 11
        elif rank == 'Q':
            rank = 10
        elif rank == 'J':
            rank = 9
        elif rank == 'T':
            rank = 8
        else:
            rank = int(rank) - 2
        suit = card[1:2]
        #convert suit ('h', 'd', 's', or 'c', to integer in range 0-3
        #0 = clubs, 1 = diamonds, 2 = hearts, 3 = spades
        if suit == 'c':
            suit = 0
        elif suit == 'd':
            suit = 1
        elif suit == 'h':
            suit = 2
        elif suit == 's':
            suit = 3
        else:
            print "Error, unknown suit"
        return suit * 13 + rank

    #decodes an integer into a string
    def decode_card(card):
        rank = card % 13
        if rank == 12:
            rank = 'A'
        elif rank == 11:
            rank = 'K'
        elif rank == 10:
            rank = 'Q'
        elif rank == 9:
            rank = 'J'
        elif rank == 8:
            rank = 'T'
        else:
            rank = rank + 2
        suit = card / 13
        if suit == 0:
            suit = 'c'
        elif suit == 1:
            suit = 'd'
        elif suit == 2:
            suit = 'h'
        elif suit == 3:
            suit = 's'
        else:
            print "Error, unknown suit"
        return "%s%s" % (rank, suit)

    #encode hand ot 32 bit integer as series of 6 4-bit nibbles
    #Each card nibble is the hex encoding of the card rank (0-12, or 1-C)
    #Type Card1 Card2 Card3 Card4 Card5, where cards 1-5 are kickers
    #Type 0 = high card hand
    #Type 1 = pair
    #Type 2 = two pair
    #Type 3 = set
    #Type 4 = straight
    #Type 5 = flush
    #Type 6 = boat
    #Type 7 = quads
    #Type 8 = straight flush
    #EX: Hand of [Ad, Td] on a board of [Ac, Kh, 4s, 2c, 9s] would
    def encode_hand(hole_cards, board):
        cards = []
        for card in hole_cards:
            cards.append(card)
        for card in board:
            cards.append(card)
        type = 0
        #store list of all possible hands, then sort to determine best hand
        hands = []
        #find straight flush
        for cmb in itertools.combinations(cards, 5):
            #decode cards to rank
            sorted_list = []
            for item in cmb:
                sorted_list.append(item % 13)
            #sort cards by rank to determine if straight
            sorted_list = bubble_sort(sorted_list)
            #check if straight
            is_straight = True
            for i in range(4):
                #if rank + 1 != rank of next card in list
                if sorted_list[i] + 1 != sorted_list[i+1]:
                    is_straight = False
                    break
            if is_straight:
                type = '4'
                hand = "0x%s%s" % (
                    type,
                    hex(sorted_list[4])[2:]
                )
                if hand not in hands:
                    hands.append(hand)

        #look for flush
        for cmb in itertools.combinations(cards, 5):
            is_flush = True
            for i in range(len(cmb) - 1):
                #different suit
                if cmb[i] / 13 != cmb[i+1] / 13:
                    is_flush = False
                    break
            if is_flush:
                #get high card in flush
                sorted_list = []
                for item in cmb:
                    sorted_list.append(item % 13)
                sorted_list = bubble_sort(sorted_list)
                high_card_rank = sorted_list[4]
                #straight flush
                if type == 4:
                    type = '9'
                #only flush
                else:
                    type = '5'
                hand = "0x%s%s" % (
                    type,
                    hex(high_card_rank)[2:]
                )
                hands.append(hand)
        #no suits necessary now
        card_ranks = []
        for card in cards:
            card_ranks.append(card % 13)
        card_ranks = bubble_sort(card_ranks)

        #find pair
        for cmb in itertools.combinations(cards, 2):
            if cmb[0] % 13 == cmb[1] % 13:
                type = '1'
                kickers = []
                for card in cards:
                    if card % 13 != cmb[0] % 13:
                        kickers.append(card % 13)
                kickers = bubble_sort(kickers)
                hand = "0x%s%s%s%s%s" % (
                    type,
                    hex(cmb[0] % 13)[2:],
                    hex(kickers[len(kickers)-1])[2:],
                    hex(kickers[len(kickers)-2])[2:],
                    hex(kickers[len(kickers)-3])[2:]
                )
                if hand not in hands:
                    hands.append(hand)
        #if pair present, look for two pair, set, boat
        #otherwise skip
        if type == '1':
            #two pair
            for cmb in itertools.combinations(card_ranks, 4):
                for perm in itertools.permutations(cmb, 4):
                    if perm[0] == perm[1] and perm[2] == perm[3]:
                        type = '2'
                        #which pair over
                        if perm[0] > perm[2]:
                            high_pair = perm[0]
                            low_pair = perm[2]
                        else:
                            high_pair = perm[2]
                            low_pair = perm[0]
                        kickers = [0]
                        for card in card_ranks:
                            if card != high_pair and card != low_pair:
                                kickers.append(card)
                        kickers = bubble_sort(kickers)
                        hand = "0x%s%s%s%s" % (
                            type,
                            hex(high_pair)[2:],
                            hex(low_pair)[2:],
                            hex(kickers[len(kickers)-1])[2:]
                        )
                        if hand not in hands:
                            hands.append(hand)

            #look for set
            for cmb in itertools.combinations(card_ranks, 3):
                if cmb[0] == cmb[1] and cmb[1] == cmb[2]:
                    #if two pair as well, full house
                    if type == '2':
                        type = '6'
                        #what full of what
                        if high_pair == cmb[0]:
                            hand = "0x%s%s%s" % (
                                type,
                                hex(cmb[0])[2:],
                                hex(low_pair)[2:]
                            )
                        else:
                            hand = "0x%s%s%s" % (
                                type,
                                hex(cmb[0])[2:],
                                hex(high_pair)[2:]
                            )
                        if hand not in hands:
                            hands.append(hand)
                    #no full house, only set
                    else:
                        type = '3'
                        kickers = []
                        for card in card_ranks:
                            if card != cmb[0]:
                                kickers.append(card)
                        kickers = bubble_sort(kickers)
                        hand = "0x%s%s%s%s" % (
                            type,
                            hex(cmb[0])[2:],
                            hex(kickers[len(kickers)-1])[2:],
                            hex(kickers[len(kickers)-2])[2:]
                        )
                        if hand not in hands:
                            hands.append(hand)
            #look for quads, skip if no set or full house
            if type == 3 or type == 6:
                for cmb in itertools.combinations(card_ranks, 4):
                    if cmb[0] == cmb[1] == cmb[2] == cmb[3]:
                        type = '7'
                        kickers = []
                        for card in card_ranks:
                            if card != cmb[0]:
                                kickers.append(card)
                        kickers = bubble_sort(kickers)
                        hand = "0x%s%s%s" % (
                            type,
                            hex(cmb[0])[2:],
                            hex(kickers[len(kickers)-1])[2:]
                        )
                        if hand not in hands:
                            hands.append(hand)
        #if high card
        if type == 0:
            kickers = []
            for card in card_ranks:
                kickers.append(card)
            kickers = bubble_sort(kickers)
            hand = "0x%s%s%s%s%s%s" % (
                type,
                hex(kickers[len(kickers)-1])[2:],
                hex(kickers[len(kickers)-2])[2:],
                hex(kickers[len(kickers)-3])[2:],
                hex(kickers[len(kickers)-4])[2:],
                hex(kickers[len(kickers)-5])[2:]
            )
            hands.append(hand)

        hands = bubble_sort(hands)
        return hands[len(hands)-1]

    #shuffle a list of cards using the Knuth shuffle algorithm
    def shuffle_deck(deck):
        for i in range(len(deck)-1, 0, -1):
            j = random.randint(0, i)
            deck[j], deck[i] = deck[i], deck[j]
        return deck

    #run game simulations against enemy range, return win rate
    def hand_strength(hole_cards, board, enemy_range, num_iters):
        #create a deck of cards
        deck = []
        for i in range(52):
            deck.append(i)
        num_wins = 0
        #remove known cards
        for card in hole_cards:
            deck.remove(card)
        for card in board:
            deck.remove(card)
        for i in range(num_iters):
            #shuffle and deal opponent hole cards
            deck = shuffle_deck(deck)
            #make a better dealing alg that supports multiple opponents
            opp_hole_cards = [deck[0], deck[1]]
            deck.pop(0)
            deck.pop(0)
            #deal remaining common cards
            common_cards = []
            for card in board:
                common_cards.append(card)
            for i in range(5 - len(board)):
                common_cards.append(deck[0])
                deck.pop(0)
            common_cards_rank = []
            for card in common_cards:
                common_cards_rank.append(card % 13)
            #print common_cards_rank
            #evaluate hands
            myhand = encode_hand(hole_cards, common_cards)
            opphand = encode_hand(opp_hole_cards, common_cards)
            if myhand > opphand:
                num_wins += 1

            #add popped out cards again
            for card in opp_hole_cards:
                deck.append(card)
            for card in common_cards:
                if card not in board:
                    deck.append(card)
        print "Hand strength: ", float(num_wins) / num_iters
        return float(num_wins) / num_iters

    def act(self, gamestate, hole_cards, board=[]):
        hole_cards[0] = encode_card(hole_cards[0])
        hole_cards[1] = encode_card(hole_cards[1])
        if board != []:
            for i in range(len(board)):
                board[i] = encode_card(board[i])
        print self.hero.stack
        print gamestate.bblind
        relative_stack = self.hero.stack / int(gamestate.bblind)
        #shove all premiums
        if hand_strength(hole_cards, board, None, 1000) >= 6.5:
            return "shove"
        if relative_stack >= 30:
            #shove premiums if over 30 BBs
            if hand_strength(hole_cards, board, None, 1000) >= 6.3:
                return "shove"

if __name__ == "__main__":
    pokerbot = AI()
    #print pokerbot.encode_card('Ah')
    #print pokerbot.decode_card(pokerbot.encode_card('Ah'))
    """for i in range(1000):
        pokerbot.encode_hand(
            pokerbot.encode_card('8h'),
            pokerbot.encode_card('Ah'),
            [
                pokerbot.encode_card('4h'),
                pokerbot.encode_card('Ac'),
                pokerbot.encode_card('Td'),
                pokerbot.encode_card('7c'),
                pokerbot.encode_card('2s')
            ]
        )"""
    pokerbot.hero = game.Player()
    mygame = game.Gamestate()
    mygame.update()
    print pokerbot.act(mygame, ['8h', '8d'], board=[])