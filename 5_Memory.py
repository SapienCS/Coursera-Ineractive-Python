# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, exposed, state, turns
    deck = [x for x in range(8)]*2
    exposed = [False]*16
    random.shuffle(deck)
    state = 0
    turns = 0


# define event handlers
def mouseclick(pos):
    global exposed, turns, state, turn1, turn2
    index = pos[0] / 50
    if not exposed[index]:
        exposed[index] = True
        if state == 0:
            turn1 = index
            state = 1
        elif state == 1:
            turn2 = index
            state = 2
            turns += 1
        else:
            if deck[turn1] != deck[turn2]:
                exposed[turn1] = exposed[turn2] = False
            turn1 = index
            state = 1


# cards are logically 50x100 pixels in size
def draw(canvas):
    label.set_text("Turns = " + str(turns))
    for each in range(16):
        x = each * 50
        if exposed[each]:
            canvas.draw_text(str(deck[each]), (x+8, 75), 70, 'White')
        else:
            canvas.draw_polygon([(0+x, 0), (50+x, 0), (50+x, 100), (0+x, 100)], 1, 'Red', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()