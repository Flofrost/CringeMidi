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
        nc.init_pair(1,  12, 20) # blue
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
    
def updateActiveMode(newMode:str, widgetsToUpdate:list[ToggleButton]) -> str:
    for w in widgetsToUpdate:
        w.state = True if w.name == newMode else False
        w.draw()
    return newMode

def getRequieredSize() -> list[int, int]:
    return [
        normalModeButton.size[0] + 
        insertModeButton.size[0] +
        visualModeButton.size[0] +
        playModeButton.size[0]   +
        projectSettingsButton.size[0]   +
        exitButton.size[0]   +
        7
        , 7
    ]
### Definition of display functions###


### Initialisation of NCurses ###
activeMode = "normal"
screen = initCringeMidi()
screenSize = screen.getmaxyx()
### Initialisation of NCurses ###


### Creation of widgets ###
normalModeButton = ToggleButton(screen=screen,
                                name="normal",
                                text=" Normal",
                                color=1)
insertModeButton = ToggleButton(screen=screen,
                                name="insert",
                                text=" Insert",
                                color=1)
visualModeButton = ToggleButton(screen=screen,
                                name="visual",
                                text="麗​Visual",
                                color=1)
playModeButton = ToggleButton(screen=screen,
                              name="play",
                              text="金​Play",
                              color=1)

projectSettingsButton = Button(screen=screen,
                               name="projectSettings",
                               text="煉​Project",
                               color=1)
exitButton = Button(screen=screen,
                    name="exit",
                    text=" Exit",
                    color=1)

statusBar = StatusBar(screen=screen,
                      name="statusBar",
                      color=2)
### Creation of widgets ###


### Compositions of widget lists ###
listOfModeButtons: list[ToggleButton] = [
    normalModeButton,
    insertModeButton,
    visualModeButton,
    playModeButton
]

listOfAllInteractibleWidgets: list[InteractibleWidget] = [
    projectSettingsButton,
    exitButton
] + listOfModeButtons

listOfAllWidgets: list[Widget] = [
    statusBar
] + listOfAllInteractibleWidgets
### Compositions of widget lists ###

### Definition of layout ###
def resetWidgetsPosition() -> None:
    normalModeButton.position      = [1,0]
    insertModeButton.position      = [normalModeButton.position[0] + normalModeButton.size[0] + 1, 0]
    visualModeButton.position      = [insertModeButton.position[0] + insertModeButton.size[0] + 1, 0]
    playModeButton.position        = [visualModeButton.position[0] + visualModeButton.size[0] + 1, 0]

    exitButton.position            = [screenSize[1] - exitButton.size[0] - 1, 0]
    projectSettingsButton.position = [exitButton.position[0] - projectSettingsButton.size[0] - 1, 0]
    
    drawAllWidgetsIn([
        Line(screen=screen,
             position=[0, 1],
             size=[screenSize[1], 0]),
        Line(screen=screen,
             position=[0, 0],
             size=[0, 2]),
        Line(screen=screen,
             position=[normalModeButton.position[0] + normalModeButton.size[0], 0],
             size=[0, 2]),
        Line(screen=screen,
             position=[insertModeButton.position[0] + insertModeButton.size[0], 0],
             size=[0, 2]),
        Line(screen=screen,
             position=[visualModeButton.position[0] + visualModeButton.size[0], 0],
             size=[0, 2]),
        Line(screen=screen,
             position=[playModeButton.position[0] + playModeButton.size[0], 0],
             size=[0, 2]),
        Line(screen=screen,
             position=[projectSettingsButton.position[0] - 1, 0],
             size=[0, 2]),
        Line(screen=screen,
             position=[exitButton.position[0] - 1, 0],
             size=[0, 2]),
        Line(screen=screen,
             position=[screenSize[1] - 1, 0],
             size=[0, 2])
    ])
### Definition of layout ###
