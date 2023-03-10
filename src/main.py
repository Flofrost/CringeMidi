#!/bin/python3
from __future__ import annotations
import curses as nc
from sys import argv
from os import path

import CringeGlobals
import CringeDisplay

try:
    import CringeEvents
    import CringeUI

    if len(argv) > 1 and path.exists(argv[1]):
        CringeUI.project.projectPath = argv[1]
        CringeUI.loadProject()
    elif len(argv) > 1:
        CringeUI.project.projectPath = argv[1] 
    else:
        CringeUI.project.projectPath = "NewProject.json"

    CringeDisplay.screen.nodelay(1)
    CringeDisplay.screen.timeout(20)
    
    CringeEvents.raiseEvent("modeUpdate", "normal")
    CringeEvents.raiseEvent("saveState")
    
    while True:
        
        event = CringeDisplay.screen.getch()
        
        CringeEvents.runScheduler()

        if event == nc.KEY_MOUSE: # Mouse Events global handler
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            CringeEvents.raiseEvent("mouseEvent", event, eventPosition)
        elif event == nc.KEY_RESIZE:
            CringeDisplay.screenResizeCheckerandUpdater()
        elif event != -1: # Keyboard events global handler
            try:
                CringeEvents.raiseEvent("keyboardEvent", CringeDisplay.convertKeyboardEvents(event))
            except CringeEvents.UnhandledKeyCode:
                CringeGlobals.debugInfo = event
            
        CringeUI.statusBar.updateText(
            f" {path.basename(CringeUI.project.projectPath)}" +
            f" {' ' + CringeGlobals.commandCombo if CringeGlobals.commandCombo else ''}",

            f"{CringeGlobals.projectSavedStatus} " +
            f"{CringeGlobals.scheduledSaveStateStatus} " +
            f"{CringeGlobals.debugInfo} "
        )

finally:
    CringeDisplay.endCringeMidi()
