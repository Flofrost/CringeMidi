#!/bin/python3
from __future__ import annotations
import curses as nc
import traceback

import CringeGlobals

try:
    import CringeEvents
    import CringeDisplay

    CringeGlobals.screen.nodelay(1)
    CringeGlobals.screen.timeout(20)
    
    CringeEvents.raiseEvent("modeUpdate", "normal")

    screenSize = CringeDisplay.screenResizeCheckerandUpdater()
    
    while True:
        
        event = CringeGlobals.screen.getch()
        
        if event == nc.KEY_MOUSE: # Mouse Events global handler
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            CringeEvents.raiseEvent("mouseEvent", event, eventPosition)
        elif event != -1: # Keyboard events global handler
            CringeEvents.raiseEvent("keyboardEvent", event)

        if nc.is_term_resized(screenSize[0], screenSize[1]): # Resize Controller
            screenSize = CringeDisplay.screenResizeCheckerandUpdater()
            
        CringeDisplay.statusBar.updateText(f" Caught: {CringeEvents.lastEvent} Uncaught: {CringeEvents.lastUncaughtEvent}", f"{CringeGlobals.debugInfo} ")

finally:
    CringeGlobals.endCringeMidi()
