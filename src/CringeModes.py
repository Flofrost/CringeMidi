from __future__ import annotations
import curses as nc

import CringeDisplay
import CringeGlobals
import CringeWidgets


def updateActiveMode(newMode:str) -> str:
    for w in CringeDisplay.listOfModeButtons:
        w.state = False
        
    CringeDisplay.screen.erase()
        
    CringeGlobals.modes[newMode]["initFunction"]()
        
    CringeDisplay.mainToolbar.draw()
    CringeWidgets.Line(
        screen=CringeDisplay.screen,
        position=[0,1],
        size=[CringeDisplay.screenSize[1],1]
    ).draw()

    CringeDisplay.fixDecorativeLines()
    CringeGlobals.activeMode = newMode

### Normal Mode ###
def initNormalMode() -> None:
    for btn in CringeDisplay.listOfModeButtons:
        if btn.name == "normal":
            btn.state = True
            break
        
    CringeDisplay.listOfAllInteractibleWidgets = CringeDisplay.mainToolbar.interactibles + CringeDisplay.normalModeToolbar.interactibles
        
    drawNormalMode()

def drawNormalMode() -> None:
    CringeDisplay.normalModeToolbar.draw()

    CringeWidgets.Line(
        screen=CringeDisplay.screen,
        position=[0,3],
        size=[CringeDisplay.screenSize[1], 1]
    ).draw()

def handleNormalModeEvents(event: int):
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
def initInsertMode() -> None:
    for btn in CringeDisplay.listOfModeButtons:
        if btn.name == "insert":
            btn.state = True
            break
    
    CringeDisplay.listOfAllInteractibleWidgets = CringeDisplay.mainToolbar.interactibles
        
    drawInsertMode()

def drawInsertMode() -> None:
    pass

def handleInsertModeEvents(event: int):
    if event == 27:
        updateActiveMode("normal")
    elif event == ord(" "):
        CringeGlobals.lastEvent = "Insert space"
### Insert Mode ###

### Help Mode ###
def initHelpMode() -> None:
    for btn in CringeDisplay.listOfModeButtons:
        if btn.name == "help":
            btn.state = True
            break
    
    CringeDisplay.listOfAllInteractibleWidgets = CringeDisplay.mainToolbar.interactibles + CringeDisplay.helpModeToolbar.interactibles
        
    drawHelpMode()

def drawHelpMode() -> None:
    CringeDisplay.helpModeToolbar.draw()

    CringeWidgets.Line(
        screen=CringeDisplay.screen,
        position=[0,3],
        size=[CringeDisplay.screenSize[1], 1]
    ).draw()
    CringeDisplay.screen.addstr(7,10,"This is the help page!")

def handleHelpModeEvents(event: int):
    if event == 27:
        updateActiveMode("normal")
### Help Mode ###