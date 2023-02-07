from __future__ import annotations
import curses as nc

import CringeDisplay
import CringeDocs
import CringeGlobals
import CringeWidgets

class Mode():
    
    def __init__(
            self,
            screen: nc._CursesWindow,
            name: str,
            widgets: list[CringeWidgets.Widget] = None,
            mouseEventHandler: function = None,
            keyboardEventHandler: function = None
        ) -> None:
        
        self.screen   = screen
        self.name     = name
        self.widgets  = widgets

        self.mouveEventsHandler    = mouseEventHandler
        self.keyboardEventsHandler = keyboardEventHandler

    def initMode(self) -> None:
        for btn in CringeDisplay.mainToolbar.interactibles[:-1]:
            if btn.name == self.name:
                btn.state = True
                break
            
        self.drawFunction()

    def drawFunction(self) -> None:
        CringeDisplay.mainToolbar.draw()
        
        for w in self.widgets:
            w.draw()
    
    def handleMouseEvents(self, event: int, eventPosition: list[int, int]) -> None:
        self.mouveEventsHandler(self, event, eventPosition)

    def handleKeyboardEvents(self, event) -> None:
        self.keyboardEventsHandler(self, event)
        
    @property
    def interactibles(self) -> list[CringeWidgets.InteractibleWidget]:
        listOfInteractibles = []
        for w in self.widgets:
            if isinstance(w, CringeWidgets.InteractibleWidget):
                listOfInteractibles.append(w)
        return listOfInteractibles
    
    

### Normal Mode ###
def normalKeyboardEvents(event: int):
    if event == ord("i"):
        updateActiveMode("insert")
    elif event == ord("H"):
        updateActiveMode("help")
    elif event == ord("u"):
        CringeGlobals.lastEvent = "undo"
    elif event == ord("r"):
        CringeGlobals.lastEvent = "redo"
### Normal Mode ###

### Insert Mode ###
def insertKeyboardEvents(event: int):
    if event == 27:
        updateActiveMode("normal")
    elif event == ord(" "):
        CringeGlobals.lastEvent = "Insert space"
### Insert Mode ###

### Help Mode ###
def helpKeyboardEvents(event: int):
    if event == 27:
        updateActiveMode("normal")
### Help Mode ###

modeList = {
    "normal" : Mode(
        screen=CringeDisplay.screen,
        name="normal",
        widgets=[
            CringeWidgets.Toolbar(
                screen=CringeDisplay.screen,
                name="normalToolbar",
                position=[0, 2],
                contents=[
                    CringeWidgets.Text(
                        screen=CringeDisplay.screen,
                        text=" ",
                    ), CringeWidgets.Button(
                        screen=CringeDisplay.screen,
                        name="undo",
                        text="社",
                        enabled=False
                    ), CringeWidgets.Text(
                        screen=CringeDisplay.screen,
                        text=" "
                    ), CringeWidgets.Button(
                        screen=CringeDisplay.screen,
                        name="redo",
                        text="漏",
                        enabled=False
                    )
                ]
            ), CringeWidgets.HLine(
                screen=CringeDisplay.screen,
                position=[0, 3],
                expand=True
            )
        ],
        mouseEventHandler=None,
        keyboardEventHandler=normalKeyboardEvents
    ),
    "insert" : Mode(
        screen=CringeDisplay.screen,
        name="insert",
        widgets=[],
        mouseEventHandler=None,
        keyboardEventHandler=insertKeyboardEvents
    ),
    "help" : Mode(
        screen=CringeDisplay.screen,
        name="help",
        widgets=[
            CringeWidgets.Toolbar(
                screen=CringeDisplay.screen,
                name="helpToolbar",
                position=[0, 2],
                contents=[
                    CringeWidgets.Text(
                        screen=CringeDisplay.screen,
                        text=" "
                    ), CringeWidgets.Button(
                        screen=CringeDisplay.screen,
                        name="prev",
                        text="<"
                    ), CringeWidgets.Expander(screen=CringeDisplay.screen),
                    CringeWidgets.Text(
                        screen=CringeDisplay.screen,
                        name="sectionName"
                    ), CringeWidgets.Expander(screen=CringeDisplay.screen),
                    CringeWidgets.Button(
                        screen=CringeDisplay.screen,
                        name="next",
                        text=">"
                    ), CringeWidgets.Text(
                        screen=CringeDisplay.screen,
                        text=" "
                    )
                ]
            ), CringeWidgets.HLine(
                screen=CringeDisplay.screen,
                position=[0, 3],
                expand=True
            )
        ],
        mouseEventHandler=None,
        keyboardEventHandler=helpKeyboardEvents
    ),
}

activeMode = modeList["normal"]

def updateActiveMode(newMode:str) -> None:
    for w in CringeDisplay.mainToolbar.interactibles[:-1]:
        w.state = False
        
    CringeDisplay.screen.erase()
        
    CringeDisplay.mainToolbar.draw()
    CringeWidgets.HLine(
        screen=CringeDisplay.screen,
        position=[0,1],
        expand=True
    ).draw()

    CringeGlobals.activeMode = modeList[newMode]
    CringeGlobals.activeMode.initMode()

    CringeDisplay.fixDecorativeLines()
