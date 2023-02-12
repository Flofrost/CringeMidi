from __future__ import annotations
import curses as nc
from signal import signal, SIGINT, SIGTERM

import CringeGlobals
import CringeMidi
import CringeWidgets


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
    
def fixDecorativeLines():
    posToFix = []
    for row in range(screenSize[0]):
        for col in range(screenSize[1]):
            if chr(screen.inch(row, col)) == "┼":
                index = 0
                if row > 0 and chr(screen.inch(row - 1, col)) in ("┼", "│"):
                    index += 1
                if col > 0 and chr(screen.inch(row, col - 1)) in ("┼", "─"):
                    index += 2
                if row < screenSize[0] - 1 and chr(screen.inch(row + 1, col)) in ("┼", "│"):
                    index += 4
                if col < screenSize[1] - 1 and chr(screen.inch(row, col + 1)) in ("┼", "─"):
                    index += 8
                posToFix.append([row, col, index])
                
    for p in posToFix:
        #                        0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
        screen.addch(p[0], p[1], (" ", " ", " ", "┘", " ", "│", "┐", "┤", " ", "└", "─", "┴", "┌", "├", "┬", "┼")[p[2]])

def redrawScreen() -> None:
    screen.erase()
    mainToolbar.draw()
    
    CringeWidgets.HLine(
        screen=screen,
        position=[0, 1],
        expand=True
    ).draw()
    
    CringeGlobals.activeMode.drawFunction()

    fixDecorativeLines()
### Definition of display functions###


### Initialisation of NCurses ###
screen = initCringeMidi()
screenSize = screen.getmaxyx()
### Initialisation of NCurses ###


### Creation of global widgets ###
mainToolbar = CringeWidgets.Layout(
    screen=screen,
    name="mainToolbar",
    position=[0, 0],
    contents=[
        CringeWidgets.VLine(
            screen=screen,
            size=2
        ),
        CringeWidgets.ToggleButton(
            screen=screen,
            name="normal",
            text="󱣱 Normal",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ),
        CringeWidgets.VLine(
            screen=screen,
            size=2
        ),
        CringeWidgets.ToggleButton(
            screen=screen,
            name="insert",
            text=" Insert",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ),
        CringeWidgets.VLine(
            screen=screen,
            size=2
        ),
        CringeWidgets.ToggleButton(
            screen=screen,
            name="play",
            text="󰐋 Play",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ),
        CringeWidgets.VLine(
            screen=screen,
            size=2
        ),
        CringeWidgets.Expander(
            screen=screen
        ),
        CringeWidgets.VLine(
            screen=screen,
            size=2
        ),
        CringeWidgets.ToggleButton(
            screen=screen,
            name="settings",
            text=" Settings",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ),
        CringeWidgets.VLine(
            screen=screen,
            size=2
        ),
        CringeWidgets.ToggleButton(
            screen=screen,
            name="help",
            text=" Help",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ),
        CringeWidgets.VLine(
            screen=screen,
            size=2
        ),
        CringeWidgets.Button(
            screen=screen,
            name="exit",
            text=" Exit",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ),
        CringeWidgets.VLine(
            screen=screen,
            size=2
        )
    ])

instrumentList: CringeMidi.InstrumentList = CringeMidi.InstrumentList(
    screen=screen,
    name="instrumentList",
    position=[0, 4]
)

workspace = [
    instrumentList,
    CringeWidgets.VLine(
        screen=screen,
        position=[21, 3],
        expand=True
    ),
]

statusBar = CringeWidgets.StatusBar(
    screen=screen,
    color=CringeGlobals.CRINGE_COLOR_PRPL
)
### Creation of global widgets ###