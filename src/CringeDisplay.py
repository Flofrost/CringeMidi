from __future__ import annotations
import curses as nc
from CringeWidgets import *


### Definition of display functions###
def initCringeMidi() -> nc._CursesWindow:
    screen = nc.initscr()
    nc.cbreak()
    nc.noecho()
    nc.start_color()
    screen.keypad(1)
    return screen

def endCringeMidi(screen:nc._CursesWindow) -> None:
    screen.keypad(0)
    nc.nocbreak()
    nc.echo()
    nc.endwin()
    exit(0)
    
def updateActiveMode(newMode:str, widgetsToUpdate:list[ToggleButton]):
    for w in widgetsToUpdate:
        w.state = True if w.name == newMode else False
        w.draw()
    return newMode
### Definition of display functions###


### Initialisation of NCurses ###
activeMode = "normal"
screen = initCringeMidi()
screenSize = screen.getmaxyx()
### Initialisation of NCurses ###


### Creation of widgets ###
normalModeButton = ToggleButton(screen=screen,
                                name="normal",
                                text=" Normal")
insertModeButton = ToggleButton(screen=screen,
                                name="insert",
                                text=" Insert")
visualModeButton = ToggleButton(screen=screen,
                                name="visual",
                                text="麗​Visual")
playModeButton = ToggleButton(screen=screen,
                              name="play",
                              text="金​Play")
projectSettingsButton = Button(screen=screen,
                               name="projectSettings",
                               text="煉​Project")
exitButton = Button(screen=screen,
                    name="exit",
                    text=" Exit")
statusBar = StatusBar(screen=screen,
                      name="statusBar",
                      justification="left",
                      color=1)
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
    
def getRequieredSize() -> list[int, int]:
    return [
        normalModeButton.size[0] + 
        insertModeButton.size[0] +
        visualModeButton.size[0] +
        playModeButton.size[0]   +
        projectSettingsButton.size[0]   +
        exitButton.size[0]   +
        7
        , 5
    ]
### Definition of layout ###
