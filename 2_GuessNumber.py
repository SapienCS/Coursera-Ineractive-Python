import random
import math
import simplegui

# initialize global variables used in your code
number_range = 100
secret_number = 0
number_of_guesses = 0


# helper function to start and restart the game
def new_game():
    global number_of_guesses, secret_number
    secret_number = random.randrange(0, number_range)
    number_of_guesses = int(math.ceil(math.log(number_range, 2)))
    print '\nNew game. Range is from 0 to', number_range
    print 'Number of remaining guesses is', number_of_guesses


# define event handlers for control panel
def range100():
    global number_range
    number_range = 100
    new_game()


def range1000():
    global number_range
    number_range = 1000
    new_game()

    
def input_guess(guess):
    # just to prevent errors while converting to int()
    # I've added a simple 'try-except' statement
    #############################################
    try:
        int(guess)
    except:
        print 'Incorrect input. Try again.'
        return
    #############################################
    global number_of_guesses
    number_of_guesses -=1
    print '\nGuess was', guess
    print 'Number of remaining guesses is', number_of_guesses
    if int(guess) == secret_number:
        print "Correct!"
        new_game() 
    elif number_of_guesses == 0: 
        print 'You ran out of guesses. The number was', secret_number
        new_game()
    elif int(guess) > secret_number:
        print 'Lower!'
    else:
        print 'Higher!'

    
# create frame

frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements

frame.add_button("range is [0, 100)", range100, 200)
frame.add_button("range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 100)

# call new_game and start frame

new_game()
frame.start()