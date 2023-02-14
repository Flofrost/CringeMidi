#!/bin/python3
from __future__ import annotations
import curses as nc
import traceback

try:
    import CringeDisplay
    import CringeGlobals
    import CringeModes

    CringeDisplay.screen.nodelay(1)
    CringeDisplay.screen.timeout(20)
    
    CringeModes.updateActiveMode("normal")

    screenSize = CringeDisplay.screenResizeCheckerandUpdater()
    
    while True:
        
        event = CringeDisplay.screen.getch()
        
        if event == nc.KEY_MOUSE: # Mouse Events global handler
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            
            for widget in CringeGlobals.mainToolbar.interactibles:
                if widget.clickHandler(event, eventPosition):
                    if widget.name == "exit":
                        CringeDisplay.terminationJudgement()
                    else:
                        CringeModes.updateActiveMode(widget.name)
                    break
            else:
                CringeGlobals.activeMode.handleMouseEvents(event, eventPosition)
        else: # Keyboard events global handler
            CringeGlobals.activeMode.handleKeyboardEvents(event)

        if nc.is_term_resized(screenSize[0], screenSize[1]): # Resize Controller
            screenSize = CringeDisplay.screenResizeCheckerandUpdater()
            
        CringeGlobals.statusBar.updateText(f" {CringeGlobals.lastEvent}", f"{CringeGlobals.debugInfo} ")

except:
    CringeDisplay.screen.keypad(0)
    nc.curs_set(1)
    nc.nocbreak()
    nc.echo()
    nc.endwin()
    traceback.print_exc()
    input()
    exit(1)
