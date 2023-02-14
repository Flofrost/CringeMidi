from __future__ import annotations
import curses as nc

import CringeGlobals
from CringeDisplay import *
from CringeWidgets import *
from CringeMidi import *

kbKeys = {
    "CTRL+LEFT": 546,
    "CTRL+RIGHT" : 561,
    "CTRL+UP" : 567,
    "CTRL+DOWN" : 526,
    "SHIFT+UP" : 337,
    "SHIFT+DOWN" : 336,
}

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
        for btn in CringeGlobals.mainToolbar.interactibles[:-1]:
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
    if event == -1:
        return
    elif event == ord("i"):
        updateActiveMode("insert")
    elif event == ord("H"):
        updateActiveMode("help")
    elif event == ord("S"):
        updateActiveMode("settings")

    elif event == ord("u"):
        CringeGlobals.lastEvent = "undo"
    elif event == ord("r"):
        CringeGlobals.lastEvent = "redo"

    elif event == ord("n"):
        CringeGlobals.sheet.addInstrument()
    elif event == ord("N"):
        if len(CringeGlobals.sheet.instrumentList) > 1:
            CringeGlobals.sheet.rmvInstrument()
    elif event == ord("J"):
        CringeGlobals.sheet.move(False)
    elif event == ord("K"):
        CringeGlobals.sheet.move()
    elif event == ord("C"):
        CringeGlobals.sheet.selectedInstrument.changeColor()
        CringeGlobals.sheet.draw()
    elif event == ord("V"):
        CringeGlobals.sheet.selectedInstrument.toggleVisible()
        CringeGlobals.sheet.draw()
    elif event == ord("T"):
        CringeGlobals.sheet.selectedInstrument.changeType()
        CringeGlobals.sheet.draw()
    elif event == ord("L"):
        CringeGlobals.sheet.selectedInstrument.changeName()
        CringeGlobals.sheet.draw()
    elif event == kbKeys["SHIFT+DOWN"]:
        CringeGlobals.sheet.selectNext()
    elif event == kbKeys["SHIFT+UP"]:
        CringeGlobals.sheet.selectNext(next=False)
        
    else:
        CringeGlobals.debugInfo = event
        
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

### Settings Mode ###
def settingsKeyboardEvents(event: int):
    if event == 27:
        updateActiveMode("normal")

def settingsMouseEvents(event: int, eventPosition: list[int, int]):
    pass
### Settings Mode ###

modeList = {
    "normal" : Mode(
        screen=screen,
        name="normal",
        widgets=[
            Layout(
                screen=screen,
                name="normalToolbar",
                position=[1, 2],
                contents=[
                    Button(
                        screen=screen,
                        name="undo",
                        text="社​",
                        enabled=False
                    ),
                    Text(
                        screen=screen,
                        text=" "
                    ),
                    Button(
                        screen=screen,
                        name="redo",
                        text="漏​",
                        enabled=False
                    ),
                ]
            ),
            CringeGlobals.sheet
        ],
        mouseEventHandler=normalMouseEvents,
        keyboardEventHandler=normalKeyboardEvents
    ),
    "insert" : Mode(
        screen=screen,
        name="insert",
        widgets=[],
        mouseEventHandler=insertMouseEvents,
        keyboardEventHandler=insertKeyboardEvents
    ),
    "settings" : Mode(
        screen=screen,
        name="settings",
        widgets=[],
        mouseEventHandler=settingsMouseEvents,
        keyboardEventHandler=settingsKeyboardEvents
    ),
    "help" : Mode(
        screen=screen,
        name="help",
        widgets=[
            Layout(
                screen=screen,
                name="helpToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=screen,
                        text=" "
                    ),
                    Button(
                        screen=screen,
                        name="prev",
                        text="<"
                    ),
                    Expander(screen=screen),
                    Text(
                        screen=screen,
                        name="sectionName"
                    ),
                    Expander(screen=screen),
                    Button(
                        screen=screen,
                        name="next",
                        text=">"
                    ),
                    Text(
                        screen=screen,
                        text=" "
                    )
                ]
            ),
            HLine(
                screen=screen,
                position=[0, 3],
                expand=True
            )
        ],
        mouseEventHandler=helpMouseEvents,
        keyboardEventHandler=helpKeyboardEvents
    )
}

def updateActiveMode(newMode:str) -> None:
    for w in CringeGlobals.mainToolbar.interactibles[:-1]:
        w.state = False
        
    screen.erase()
        
    CringeGlobals.activeMode = modeList[newMode]
    CringeGlobals.activeMode.initMode()

    CringeGlobals.mainToolbar.draw()
    CringeGlobals.mainToolBarLine.draw()

    fixDecorativeLines()
