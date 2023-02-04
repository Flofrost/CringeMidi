#!/bin/python3
from __future__ import annotations
import curses as nc

import CringeDisplay
import CringeGlobals
import CringeMidi
import CringeMisc
import CringeModes
import CringeWidgets


if __name__ == "__main__":

    CringeDisplay.screen.nodelay(1)
    CringeDisplay.screen.timeout(20)
    
    CringeDisplay.updateActiveMode("normal")
    CringeDisplay.redrawScreen()
    CringeDisplay.fixDecorativeLines()
    
    while True:
        
        event = CringeDisplay.screen.getch()
        
        if event == nc.KEY_MOUSE:
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            
            for widget in CringeDisplay.listOfAllInteractibleWidgets:
                if widget.clicked(event, eventPosition):
                    
                    if widget.name == "exit":
                        CringeDisplay.terminationJudgement()
                    elif widget in CringeDisplay.listOfModeButtons:
                        CringeModes.updateActiveMode(widget.name)
        else:
            CringeGlobals.modes[CringeGlobals.activeMode]["eventHandler"](event)

        if nc.is_term_resized(CringeDisplay.screenSize[0], CringeDisplay.screenSize[1]): # Resize Controller
            CringeDisplay.screen.clear()
            CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
            minSize = [CringeDisplay.mainToolbar.size[0], 10]
            minW = CringeDisplay.screenSize[1] - minSize[0]
            minH = CringeDisplay.screenSize[0] - minSize[1]
            
            while minW < 0 or minH < 0:
                CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
                minSize = [CringeDisplay.mainToolbar.size[0], 13]
                minW = CringeDisplay.screenSize[1] - minSize[0]
                minH = CringeDisplay.screenSize[0] - minSize[1]

                CringeDisplay.screen.addch(0, 0, "")
                CringeDisplay.screen.refresh()

            CringeDisplay.redrawScreen()
            CringeDisplay.fixDecorativeLines()
            
        CringeDisplay.statusBar.updateText(f"{CringeGlobals.lastEvent} {CringeGlobals.debugInfo}")
