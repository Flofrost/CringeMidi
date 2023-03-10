#!/bin/python3
from __future__ import annotations
import curses as nc
from sys import argv
from os import path

import CringeGlobals

try:
    import CringeEvents
    import CringeDisplay

    if len(argv) > 1 and path.exists(argv[1]):
        CringeDisplay.project.projectPath = argv[1]
        CringeDisplay.loadProject()
    elif len(argv) > 1:
        CringeDisplay.project.projectPath = argv[1] 
    else:
        CringeDisplay.project.projectPath = "NewProject.json"

    CringeGlobals.screen.nodelay(1)
    CringeGlobals.screen.timeout(20)
    
    CringeEvents.raiseEvent("modeUpdate", "normal")
    CringeEvents.raiseEvent("saveState")

    screenSize = CringeDisplay.screenResizeCheckerandUpdater()
    
    while True:
        
        event = CringeGlobals.screen.getch()
        
        CringeEvents.runScheduler()

        if event == nc.KEY_MOUSE: # Mouse Events global handler
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            CringeEvents.raiseEvent("mouseEvent", event, eventPosition)
        elif event != -1: # Keyboard events global handler
            CringeEvents.raiseEvent("keyboardEvent", event)

        if nc.is_term_resized(screenSize[0], screenSize[1]): # Resize Controller
            screenSize = CringeDisplay.screenResizeCheckerandUpdater()
            
        CringeDisplay.statusBar.updateText(f" {path.basename(CringeDisplay.project.projectPath)} {' ' + CringeGlobals.commandCombo if CringeGlobals.commandCombo else ''}", f"{CringeGlobals.projectSavedStatus} {CringeGlobals.scheduledSaveStateStatus} {CringeGlobals.debugInfo} ")

finally:
    CringeGlobals.endCringeMidi()
