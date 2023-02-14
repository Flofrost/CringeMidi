from __future__ import annotations
import curses as nc
from signal import signal, SIGINT, SIGTERM

import CringeGlobals

### Definition of display functions###
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
        nc.init_pair(CringeGlobals.CRINGE_COLOR_BLUE,  39, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_PRPL, 135, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_DSBL, 245, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[0], 196, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[1],  40, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[2],  27, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[3], 200, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[4], 220, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[5],  51, -1)

    nc.mousemask(-1)
    
    signal(SIGINT, terminationJudgement)
    signal(SIGTERM, terminationJudgement)

    return screen

def terminationJudgement(*args):
    endCringeMidi(screen=screen)

def endCringeMidi(screen:nc._CursesWindow) -> None:
    screen.keypad(0)
    nc.curs_set(1)
    nc.nocbreak()
    nc.echo()
    nc.endwin()
    exit(0)
    
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

def fixDecorativeLines():
    posToFix = []
    for row in range(screen.getmaxyx()[0]):
        for col in range(screen.getmaxyx()[1]):
            if chr(screen.inch(row, col)) == "┼":
                index = 0
                if row > 0 and chr(screen.inch(row - 1, col)) in ("┼", "│"):
                    index += 1
                if col > 0 and chr(screen.inch(row, col - 1)) in ("┼", "─"):
                    index += 2
                if row < screen.getmaxyx()[0] - 1 and chr(screen.inch(row + 1, col)) in ("┼", "│"):
                    index += 4
                if col < screen.getmaxyx()[1] - 1 and chr(screen.inch(row, col + 1)) in ("┼", "─"):
                    index += 8
                posToFix.append([row, col, index])
                
    for p in posToFix:
        #                        0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
        screen.addch(p[0], p[1], (" ", " ", " ", "┘", " ", "│", "┐", "┤", " ", "└", "─", "┴", "┌", "├", "┬", "┼")[p[2]])

def redrawScreen() -> None:
    screen.erase()

    CringeGlobals.mainToolbar.draw()
    CringeGlobals.mainToolBarLine.draw()
    CringeGlobals.activeMode.drawFunction()

    fixDecorativeLines()

def screenResizeCheckerandUpdater() -> list[int, int]:
    minW = screen.getmaxyx()[1] - CringeGlobals.mainToolbar.size[0]
    minH = screen.getmaxyx()[0] - 15
    
    while minW < 0 or minH < 0:
        minW = screen.getmaxyx()[1] - CringeGlobals.mainToolbar.size[0] - 2
        minH = screen.getmaxyx()[0] - 15 - 2

        screen.erase()
        screen.addch(0, 0, "")
        screen.refresh()

    redrawScreen()
    
    return screen.getmaxyx()
### Definition of display functions###


### Initialisation of NCurses ###
screen = initCringeMidi()
### Initialisation of NCurses ###