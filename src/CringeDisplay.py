from __future__ import annotations
import curses as nc
from signal import signal, SIGINT, SIGTERM
from CringeWidgets import *


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
        nc.init_pair(1,  39, -1) # blue
        nc.init_pair(2, 135, -1) # purple

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
    
def updateActiveMode(newMode:str) -> str:
    for w in listOfModeButtons:
        if w.name == newMode:
            w.state = True
        else:
            w.state = False
        w.draw()
    return newMode

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
### Definition of display functions###


### Initialisation of NCurses ###
activeMode = "normal"
screen = initCringeMidi()
screenSize = screen.getmaxyx()
### Initialisation of NCurses ###


### Creation of widgets ###
mainToolbar = Toolbar(screen=screen,
                      name="mainToolbar",
                      contents=[
                        Line(screen=screen,
                             size=[1, 2]),
                        ToggleButton(screen=screen,
                                     name="normal",
                                     text=" Normal",
                                     color=1),
                        Line(screen=screen,
                             size=[1, 2]),
                        ToggleButton(screen=screen,
                                     name="insert",
                                     text=" Insert",
                                     color=1),
                        Line(screen=screen,
                             size=[1, 2]),
                        ToggleButton(screen=screen,
                                     name="play",
                                     text="金​Play",
                                     color=1),
                        Line(screen=screen,
                             size=[1, 2]),
                        Expander(screen=screen),
                        Line(screen=screen,
                             size=[1, 2]),
                        ToggleButton(screen=screen,
                                     name="projectSettings",
                                     text="煉​Project",
                                     color=1),
                        Line(screen=screen,
                             size=[1, 2]),
                        ToggleButton(screen=screen,
                                     name="help",
                                     text=" Help",
                                     color=1),
                        Line(screen=screen,
                             size=[1, 2]),
                        Button(screen=screen,
                                name="exit",
                                text=" Exit",
                                color=1),
                        Line(screen=screen,
                             size=[1, 2]),
                      ],
                      position=[0,0])

undoButton = Button(screen=screen,
                    name="undo",
                    text="社",
                    enabled=False)
redoButton = Button(screen=screen,
                    name="redo",
                    text="漏",
                    enabled=False)

statusBar = StatusBar(screen=screen,
                      color=2)
### Creation of widgets ###


### Compositions of widget lists ###
listOfModeButtons = mainToolbar.interactibles[:-1]

listOfNormalToolbar: list[Button] = [
    undoButton,
    redoButton
]

listOfAllInteractibleWidgets: list[InteractibleWidget] = [
] + mainToolbar.interactibles

listOfAllWidgets: list[Widget] = [
    mainToolbar,
    statusBar
]
### Compositions of widget lists ###

### Definition of layout ###
def updateWidgetsPosition() -> None:
    
    mainToolbar.updateWidgetsPosition()

    drawAllWidgetsIn([ # Decorative lines
        Line(screen=screen,
             position=[0,1],
             size=[screenSize[1],1]),
        Line(screen=screen,
             position=[0,3],
             size=[screenSize[1],1])
    ])
### Definition of layout ###
