from __future__ import annotations
import curses as nc

import CringeDisplay
import CringeDocs
import CringeGlobals
from CringeWidgets import *

class Mode():
    
    def __init__(
            self,
            screen: nc._CursesWindow,
            name: str,
            widgets: list[Widget] = None,
            mouseEventHandler: function = None,
            keyboardEventHandler: function = None
        ) -> None:
        
        self.screen   = screen
        self.name     = name
        self.widgets  = widgets

        self.mouseEventsHandler    = mouseEventHandler
        self.keyboardEventsHandler = keyboardEventHandler

    def initMode(self) -> None:
        for btn in CringeDisplay.mainToolbar.interactibles[:-1]:
            if btn.name == self.name:
                btn.state = True
                break
            
        self.drawFunction()

    def drawFunction(self) -> None:
        for w in self.widgets:
            w.draw()
    
    def handleMouseEvents(self, event: int, eventPosition: list[int, int]) -> None:
        self.mouseEventsHandler(event, eventPosition)

    def handleKeyboardEvents(self, event: int) -> None:
        self.keyboardEventsHandler(event)
        
    @property
    def interactibles(self) -> list[InteractibleWidget]:
        listOfInteractibles = []
        for w in self.widgets:
            if isinstance(w, Layout):
                listOfInteractibles += w.interactibles
            elif isinstance(w, InteractibleWidget):
                listOfInteractibles.append(w)
        return listOfInteractibles

### Normal Mode ###
def normalKeyboardEvents(event: int):
    if event == ord("i"):
        updateActiveMode("insert")
    elif event == ord("H"):
        updateActiveMode("help")
    elif event == ord("m"):
        updateActiveMode("play")
    elif event == ord("S"):
        updateActiveMode("settings")
    elif event == ord("u"):
        CringeGlobals.lastEvent = "undo"
    elif event == ord("r"):
        CringeGlobals.lastEvent = "redo"
        
def normalMouseEvents(event: int, eventPosition: list[int, int]):
    for w in modeList["normal"].interactibles:
        eventStr = w.clicked(event, eventPosition)
        if eventStr:
            CringeGlobals.lastEvent = eventStr
### Normal Mode ###

### Insert Mode ###
def insertKeyboardEvents(event: int):
    if event == 27:
        updateActiveMode("normal")
    elif event == ord(" "):
        CringeGlobals.lastEvent = "Insert space"

def insertMouseEvents(event: int, eventPosition: list[int, int]):
    for w in modeList["insert"].interactibles:
        if w.clicked(event, eventPosition):
            CringeGlobals.lastEvent = w.name
### Insert Mode ###

### Help Mode ###
def helpKeyboardEvents(event: int):
    if event == 27:
        updateActiveMode("normal")

def helpMouseEvents(event: int, eventPosition: list[int, int]):
    pass
### Help Mode ###

### Play Mode ###
def playKeyboardEvents(event: int):
    if event == 27:
        updateActiveMode("normal")

def playMouseEvents(event: int, eventPosition: list[int, int]):
    for w in modeList["play"].interactibles:
        if w.clicked(event, eventPosition):
            CringeGlobals.lastEvent = w.name
### Play Mode ###

### Settings Mode ###
def settingsKeyboardEvents(event: int):
    if event == 27:
        updateActiveMode("normal")

def settingsMouseEvents(event: int, eventPosition: list[int, int]):
    pass
### Settings Mode ###

modeList = {
    "normal" : Mode(
        screen=CringeDisplay.screen,
        name="normal",
        widgets=[
            Layout(
                screen=CringeDisplay.screen,
                name="normalToolbar",
                position=[1, 2],
                contents=[
                    Button(
                        screen=CringeDisplay.screen,
                        name="undo",
                        text="社​",
                        enabled=False
                    ),
                    Text(
                        screen=CringeDisplay.screen,
                        text=" "
                    ),
                    Button(
                        screen=CringeDisplay.screen,
                        name="redo",
                        text="漏​",
                        enabled=False
                    ),
                ]
            ),
            HLine(
                screen=CringeDisplay.screen,
                position=[0, 3],
                expand=True
            )
        ] + CringeDisplay.workspace,
        mouseEventHandler=normalMouseEvents,
        keyboardEventHandler=normalKeyboardEvents
    ),
    "insert" : Mode(
        screen=CringeDisplay.screen,
        name="insert",
        widgets=[] + CringeDisplay.workspace,
        mouseEventHandler=insertMouseEvents,
        keyboardEventHandler=insertKeyboardEvents
    ),
    "play" : Mode(
        screen=CringeDisplay.screen,
        name="play",
        widgets=[] + CringeDisplay.workspace,
        mouseEventHandler=playMouseEvents,
        keyboardEventHandler=playKeyboardEvents
    ),
    "settings" : Mode(
        screen=CringeDisplay.screen,
        name="settings",
        widgets=[],
        mouseEventHandler=settingsMouseEvents,
        keyboardEventHandler=settingsKeyboardEvents
    ),
    "help" : Mode(
        screen=CringeDisplay.screen,
        name="help",
        widgets=[
            Layout(
                screen=CringeDisplay.screen,
                name="helpToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=CringeDisplay.screen,
                        text=" "
                    ),
                    Button(
                        screen=CringeDisplay.screen,
                        name="prev",
                        text="<"
                    ),
                    Expander(screen=CringeDisplay.screen),
                    Text(
                        screen=CringeDisplay.screen,
                        name="sectionName"
                    ),
                    Expander(screen=CringeDisplay.screen),
                    Button(
                        screen=CringeDisplay.screen,
                        name="next",
                        text=">"
                    ),
                    Text(
                        screen=CringeDisplay.screen,
                        text=" "
                    )
                ]
            ),
            HLine(
                screen=CringeDisplay.screen,
                position=[0, 3],
                expand=True
            )
        ],
        mouseEventHandler=helpMouseEvents,
        keyboardEventHandler=helpKeyboardEvents
    )
}

CringeGlobals.activeMode: Mode = modeList["normal"]

def updateActiveMode(newMode:str) -> None:
    for w in CringeDisplay.mainToolbar.interactibles[:-1]:
        w.state = False
        
    CringeDisplay.screen.erase()
        
    CringeGlobals.activeMode = modeList[newMode]
    CringeGlobals.activeMode.initMode()

    CringeDisplay.mainToolbar.draw()
    HLine(
        screen=CringeDisplay.screen,
        position=[0,1],
        expand=True
    ).draw()

    CringeDisplay.fixDecorativeLines()
