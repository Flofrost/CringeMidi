#!/bin/python3
from __future__ import annotations
import curses as nc

import CringeDisplay
import CringeGlobals
import CringeModes


if __name__ == "__main__":

    CringeDisplay.screen.nodelay(1)
    CringeDisplay.screen.timeout(20)
    
    CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
    minSize = [CringeDisplay.mainToolbar.size[0], 15]
    minW = CringeDisplay.screenSize[1] - minSize[0]
    minH = CringeDisplay.screenSize[0] - minSize[1]
    
    while minW < 0 or minH < 0:
        CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
        minSize = [CringeDisplay.mainToolbar.size[0] + 2, 17]
        minW = CringeDisplay.screenSize[1] - minSize[0]
        minH = CringeDisplay.screenSize[0] - minSize[1]

        CringeDisplay.screen.erase()
        CringeDisplay.screen.addch(0, 0, "")
        CringeDisplay.screen.refresh()

    CringeModes.updateActiveMode("normal")
    CringeDisplay.redrawScreen()
    
    while True:
        
        event = CringeDisplay.screen.getch()
        
        if event == nc.KEY_MOUSE: # Mouse Events global handler
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            
            for widget in CringeDisplay.mainToolbar.interactibles:
                if widget.clicked(event, eventPosition):
                    if widget.name == "exit":
                        CringeDisplay.terminationJudgement()
                    else:
                        CringeModes.updateActiveMode(widget.name)
                    break
            else:
                CringeGlobals.activeMode.handleMouseEvents(event, eventPosition)
        else: # Keyboard events global handler
            CringeGlobals.activeMode.handleKeyboardEvents(event)

        if nc.is_term_resized(CringeDisplay.screenSize[0], CringeDisplay.screenSize[1]): # Resize Controller
            CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
            minSize = [CringeDisplay.mainToolbar.size[0], 15]
            minW = CringeDisplay.screenSize[1] - minSize[0]
            minH = CringeDisplay.screenSize[0] - minSize[1]
            
            while minW < 0 or minH < 0:
                CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
                minSize = [CringeDisplay.mainToolbar.size[0] + 2, 17]
                minW = CringeDisplay.screenSize[1] - minSize[0]
                minH = CringeDisplay.screenSize[0] - minSize[1]

                CringeDisplay.screen.erase()
                CringeDisplay.screen.addch(0, 0, "")
                CringeDisplay.screen.refresh()

            CringeDisplay.redrawScreen()
            
        CringeDisplay.statusBar.updateText(f"{CringeGlobals.lastEvent} {CringeGlobals.debugInfo}")
