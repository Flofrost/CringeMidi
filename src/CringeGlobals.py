from __future__ import annotations
import curses as nc
from signal import signal, SIGINT, SIGTERM
import traceback

from CringeEvents import *

CRINGE_COLOR_BLUE = 1
CRINGE_COLOR_PRPL = 2
CRINGE_COLOR_DSBL = 3
CRINGE_COLOR_ISTR = [10, 11, 12, 13, 14, 15, 16, 17, 18]

CRINGE_ISTR_TYPES = [
    "sine",
    "square",
    "triangle",
    "noise"
]

debugInfo = ""

def initCringeMidi() -> nc._CursesWindow:
    screen = nc.initscr()
    nc.cbreak()
    nc.noecho()
    nc.curs_set(0)
    nc.mouseinterval(0)
    nc.set_escdelay(100)
    screen.keypad(1)

    if nc.has_colors():
        nc.start_color()
        nc.use_default_colors()
        nc.init_pair(CRINGE_COLOR_BLUE,  39, -1)
        nc.init_pair(CRINGE_COLOR_PRPL, 135, -1)
        nc.init_pair(CRINGE_COLOR_DSBL, 245, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[0], 196, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[1],  40, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[2],  27, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[3], 200, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[4], 220, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[5],  51, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[6], 202, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[7],  22, -1)
        nc.init_pair(CRINGE_COLOR_ISTR[8],  93, -1)

    nc.mousemask(-1)
    
    signal(SIGINT, terminationJudgement)
    signal(SIGTERM, terminationJudgement)

    return screen

def terminationJudgement(*args):
    endCringeMidi()

def endCringeMidi() -> None:
    screen.keypad(0)
    nc.curs_set(1)
    nc.nocbreak()
    nc.echo()
    nc.endwin()
    traceback.print_exc()
    exit(0)

screen = initCringeMidi()

subscribe("exit", terminationJudgement)

def getInput(prompt: str = "", limit: int = 50, attributes: int = 0) -> str | None:
    screen.timeout(-1)
    
    string = ""
    while True:
        screen.addstr(screen.getmaxyx()[0] - 1, 0, " " * (screen.getmaxyx()[1] - 1), attributes)
        screen.addstr(screen.getmaxyx()[0] - 1, 0, f" {prompt}{string}_", attributes)

        event = screen.getkey()
        if event == "\x1b": # Escape
            string = None
            break
        elif event == "\n": # Return
            if not len(string):
                string = None
            break
        elif event == "KEY_BACKSPACE": # Backspace
            if len(string) > 1:
                string = string[:len(string)-1]
            else:
                string = ""
        elif event.isprintable() and len(event) == 1:
            if len(string) < limit:
                string += event
    screen.timeout(20)

    return string