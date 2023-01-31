from __future__ import annotations
import curses as nc
from CringeWidgets import *

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
    global activeMode
    activeMode = newMode
    for w in widgetsToUpdate:
        w.state = True if w.name == newMode else False
        w.draw()

activeMode = "normal"
screen = initCringeMidi()
screenSize = screen.getmaxyx()

listOfModeButtons: InteractibleWidget = [
    ToggleButton(screen=screen,
                               position=[1,0],
                               name="normal",
                               text=" Normal"),
    ToggleButton(screen=screen,
                               position=[10,0],
                               name="insert",
                               text=" Insert"),
    ToggleButton(screen=screen,
                               position=[20,0],
                               name="visual",
                               text="麗​ Visual"),
    ToggleButton(screen=screen,
                               position=[31,0],
                               name="play",
                               text="金​ Play")
]

topButtons = listOfModeButtons + [
    Button(screen=screen,
                         position=[screenSize[1] - 11 - 8, 0],
                         name="projectSettings",
                         text="煉 Project"),
    Button(screen=screen,
                         position=[screenSize[1] - 8, 0],
                         name="exit",
                         text=" Exit")
]

listOfAllInteractibleWidgets = topButtons

statusBar = StatusBar(screen=screen,
                                    name="statusBar",
                                    justification="left",
                                    color=1)

listOfAllWidgets: Widget = [
    statusBar
] + listOfAllInteractibleWidgets