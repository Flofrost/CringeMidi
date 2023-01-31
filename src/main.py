#!/bin/python3
from __future__ import annotations
import curses as nc

import CringeDisplay
import CringeMidi
import CringeMisc
import CringeWidgets


if __name__ == "__main__":

    if nc.has_colors():
        nc.use_default_colors()
        nc.init_pair(1, 135, -1)

    nc.mousemask(-1)

    CringeDisplay.screen.nodelay(1)
    CringeDisplay.screen.timeout(20)
    
    CringeDisplay.updateActiveMode("normal", CringeDisplay.listOfModeButtons)
    CringeWidgets.drawAllWidgetsIn(CringeDisplay.listOfAllWidgets)
    
    while True:
        
        event = CringeDisplay.screen.getch()
        
        if event == nc.KEY_MOUSE:
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            
            for widget in CringeDisplay.listOfAllInteractibleWidgets:
                if widget.clicked(event, eventPosition):
                    
                    if widget.name == "exit":
                        CringeDisplay.endCringeMidi(CringeDisplay.screen)
                    elif widget in CringeDisplay.listOfModeButtons:
                        CringeDisplay.updateActiveMode(widget.name, CringeDisplay.listOfModeButtons)

        elif event == 27 and CringeDisplay.activeMode != "normal":
            CringeDisplay.updateActiveMode("normal", CringeDisplay.listOfModeButtons)
        elif event == ord("i"):
            CringeDisplay.updateActiveMode("insert", CringeDisplay.listOfModeButtons)
        elif event == ord("v"):
            CringeDisplay.updateActiveMode("visual", CringeDisplay.listOfModeButtons)
        elif event == ord("m"):
            CringeDisplay.updateActiveMode("play", CringeDisplay.listOfModeButtons)

        if nc.is_term_resized(CringeDisplay.screenSize[0], CringeDisplay.screenSize[1]):
            CringeDisplay.screen.clear()
            CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
            
            CringeWidgets.drawAllWidgetsIn(CringeDisplay.listOfAllWidgets)
            
        # statusBar.updateText(f"")