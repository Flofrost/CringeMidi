from __future__ import annotations
import curses as nc
from signal import signal, SIGINT, SIGTERM

import CringeGlobals
import CringeWidgets


### Definition of display functions###
def initCringeMidi() -> nc._CursesWindow:
    screen = nc.initscr()
    nc.cbreak()
    nc.noecho()
    nc.curs_set(0)
    nc.set_escdelay(100)
    screen.keypad(1)

    if nc.has_colors():
        nc.start_color()
        nc.use_default_colors()
        nc.init_pair(CringeGlobals.CRINGE_COLOR_BLUE,  39, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_PRPL, 135, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_DSBL, 240, -1)

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
                #                        0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
                screen.addch(row, col, (" ", " ", " ", "┘", " ", "│", "┐", "┤", " ", "└", "─", "┴", "┌", "├", "┬", "┼")[index])

def redrawScreen() -> None:
    screen.erase()
    mainToolbar.draw()
    
    CringeGlobals.modes[CringeGlobals.activeMode]["drawFunction"]()

    CringeWidgets.Line(
        screen=screen,
        position=[0,1],
        size=[screenSize[1],1]
    ).draw()
    
    fixDecorativeLines()
### Definition of display functions###


### Initialisation of NCurses ###
screen = initCringeMidi()
screenSize = screen.getmaxyx()
### Initialisation of NCurses ###


### Creation of widgets ###
mainToolbar = CringeWidgets.Toolbar(
    screen=screen,
    name="mainToolbar",
    position=[0, 0],
    contents=[
        CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        ), CringeWidgets.ToggleButton(
            screen=screen,
            name="normal",
            text=" Normal",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ), CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        ), CringeWidgets.ToggleButton(
            screen=screen,
            name="insert",
            text=" Insert",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ), CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        ), CringeWidgets.ToggleButton(
            screen=screen,
            name="play",
            text="金​Play",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ), CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        ),
        CringeWidgets.Expander(screen=screen),
        CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        ), CringeWidgets.ToggleButton(
            screen=screen,
            name="settings",
            text="煉​Settings",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ), CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        ), CringeWidgets.ToggleButton(
            screen=screen,
            name="help",
            text=" Help",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ), CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        ), CringeWidgets.Button(
            screen=screen,
            name="exit",
            text=" Exit",
            color=CringeGlobals.CRINGE_COLOR_BLUE
        ), CringeWidgets.Line(
            screen=screen,
            size=[1, 2]
        )
    ])

normalModeToolbar = CringeWidgets.Toolbar(
    screen=screen,
    name="normalToolbar",
    position=[0, 2],
    contents=[
        CringeWidgets.Text(
            screen=screen,
            text=" ",
        ), CringeWidgets.Button(
            screen=screen,
            name="undo",
            text="社",
            enabled=False
        ), CringeWidgets.Text(
            screen=screen,
            text=" "
        ), CringeWidgets.Button(
            screen=screen,
            name="redo",
            text="漏",
            enabled=False
        )
    ]
)

helpModeToolbar = CringeWidgets.Toolbar(
    screen=screen,
    name="helpToolbar",
    position=[0, 2],
    contents=[
        CringeWidgets.Text(
            screen=screen,
            text=" "
        ), CringeWidgets.Button(
            screen=screen,
            name="prev",
            text="<"
        ), CringeWidgets.Expander(screen=screen),
        CringeWidgets.Text(
            screen=screen,
            name="sectionName"
        ), CringeWidgets.Expander(screen=screen),
        CringeWidgets.Button(
            screen=screen,
            name="next",
            text=">"
        ), CringeWidgets.Text(
            screen=screen,
            text=" "
        )
    ]
)

statusBar = CringeWidgets.StatusBar(screen=screen,
                      color=CringeGlobals.CRINGE_COLOR_PRPL)
### Creation of widgets ###


### Compositions of widget lists ###
listOfModeButtons = mainToolbar.interactibles[:-1]

listOfAllInteractibleWidgets: list[CringeWidgets.InteractibleWidget] = mainToolbar.interactibles
### Compositions of widget lists ###