# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
outcome2 = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.hand_value = 0

    def __str__(self):
        result = 'Hand contains '
        for each in self.cards:
            result += ' ' + str(each)
        return result

    def __ge__(self, other):
        return self.get_value() >= other.get_value()

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        self.hand_value = sum([VALUES[card.get_rank()] for card in self.cards])
        ace_in = any([card.get_rank() == 'A' for card in self.cards])
        if ace_in and self.hand_value <= 11:
            self.hand_value += 10
        return self.hand_value

    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 90


# define deck class
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        result = 'Deck contains'
        for each in self.deck:
            result += ' '+ str(each)
        return result



#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand
    global outcome2, deck, score
    outcome = ''
    if in_play:
        score -= 1
        outcome = 'You lose.'
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    in_play = True


def hit():
    global player_hand, in_play, outcome, score, outcome2
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = 'You went bust and lose.'
            outcome2 = 'New deal?'
            score -= 1
            in_play = False


def stand():
    global dealer_hand, in_play, outcome, score, outcome2
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
           dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer busts and lose'
            score += 1
        elif dealer_hand >= player_hand:
            outcome = 'Dealer win'
            score -= 1
        else:
            outcome = 'You win'
            score += 1
        outcome2 = 'New deal?'


# draw handler
def draw(canvas):
    global outcome2
    canvas.draw_text('Blackjack', [100, 80], 50, 'White')
    score_text = 'Score ' + str(score)
    canvas.draw_text(score_text, [400, 80], 30, 'Black')
    canvas.draw_text('Dealer', [80, 130], 30, 'Black')
    canvas.draw_text('Player', [80, 330], 30, 'Black')
    dealer_hand.draw(canvas,[80, 160])
    player_hand.draw(canvas,[80, 360])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [80+CARD_CENTER[0], 160+CARD_CENTER[1]], CARD_BACK_SIZE)
        outcome2 = 'Hit or stand?'
    canvas.draw_text(outcome, [210, 130], 30, 'Black')
    canvas.draw_text(outcome2, [210, 330], 30, 'Black')



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

