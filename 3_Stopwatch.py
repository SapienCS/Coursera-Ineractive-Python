import simplegui

# define global variables
time_counter = 0
tries = 0
wins = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    a = t / 600
    b = (t / 100) % 6
    c = (t / 10) % 10
    d = t % 10
    return str(a) + ":" + str(b) + str(c) + "." + str(d)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start_watch():
    if not timer.is_running():
        timer.start()


def stop_watch():
    global tries, wins
    if timer.is_running():
        timer.stop()
        tries += 1
        if time_counter % 10 == 0:
            wins += 1


def reset_watch():
    global time_counter, tries, wins
    timer.stop()
    time_counter = 0
    tries = 0
    wins = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global time_counter
    time_counter += 1


# define draw handler
def draw(canvas):
    games_string = str(wins) + "/" + str(tries)
    canvas.draw_text(format(time_counter), [105, 110], 40, "Red")
    canvas.draw_text(games_string, [250, 30], 25, "Green")

# create frame and timer
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start_watch, 100)
frame.add_button("Stop", stop_watch, 100)
frame.add_button("Reset", reset_watch, 100)

# start frame
frame.start()