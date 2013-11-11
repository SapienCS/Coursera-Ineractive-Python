# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
POFFSET = 3

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    xvel = random.randrange(120, 240) / 60
    yvel = random.randrange(60, 180) / 60
    if direction:
        ball_dir = 1
    else:
        ball_dir = -1
    ball_vel = [ball_dir * xvel, -yvel]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel 
    global score1, score2
    score1, score2 = 0, 0
    paddle1_vel, paddle2_vel = 0, 0
    paddle1_pos, paddle2_pos = HEIGHT / 2, HEIGHT / 2 
    spawn_ball(random.randrange(2))

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1 
    if abs(ball_pos[1] - paddle1_pos) <= HALF_PAD_HEIGHT and ball_pos[0] <= BALL_RADIUS + PAD_WIDTH \
    or abs(ball_pos[1] - paddle2_pos) <= HALF_PAD_HEIGHT and ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        ball_vel = [x*1.1 for x in ball_vel]
        ball_vel[0] *= -1
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        score1 += 1
        spawn_ball(LEFT)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, 'Blue', 'White')
    # update paddle's vertical position, keep paddle on the screen
    if HEIGHT - HALF_PAD_HEIGHT > paddle1_pos + paddle1_vel > HALF_PAD_HEIGHT - 1: 
        paddle1_pos += paddle1_vel    
    if HEIGHT - HALF_PAD_HEIGHT > paddle2_pos + paddle2_vel > HALF_PAD_HEIGHT - 1: 
        paddle2_pos += paddle2_vel
    # draw paddles
    c.draw_line((HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), PAD_WIDTH, 'WHITE')
    c.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), PAD_WIDTH, 'WHITE')
    # draw scores
    c.draw_text(str(score1), (WIDTH / 2 - 100, 100), 50, 'White')
    c.draw_text(str(score2), (WIDTH / 2 + 75, 100), 50, 'White')
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= POFFSET
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += POFFSET   
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= POFFSET
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += POFFSET     
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += POFFSET
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel -= POFFSET 
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += POFFSET
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= POFFSET

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 100)

# start frame
new_game()
frame.start()
