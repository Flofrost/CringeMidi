#!/bin/python3
from __future__ import annotations
import curses as nc

import CringeDisplay
import CringeMidi
import CringeMisc
import CringeWidgets


if __name__ == "__main__":

    CringeDisplay.screen.nodelay(1)
    CringeDisplay.screen.timeout(20)
    
    CringeDisplay.activeMode = CringeDisplay.updateActiveMode("normal", CringeDisplay.listOfModeButtons)
    CringeDisplay.resetWidgetsPosition()
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
                        CringeDisplay.terminationJudgement()
                    elif widget in CringeDisplay.listOfModeButtons:
                        CringeDisplay.updateActiveMode(widget.name, CringeDisplay.listOfModeButtons)

        elif event == 27 and CringeDisplay.activeMode != "normal":
            CringeDisplay.activeMode = CringeDisplay.updateActiveMode("normal", CringeDisplay.listOfModeButtons)
        elif event == ord("i"):
            CringeDisplay.activeMode = CringeDisplay.updateActiveMode("insert", CringeDisplay.listOfModeButtons)
        elif event == ord("v"):
            CringeDisplay.activeMode = CringeDisplay.updateActiveMode("visual", CringeDisplay.listOfModeButtons)
        elif event == ord("m"):
            CringeDisplay.activeMode = CringeDisplay.updateActiveMode("play", CringeDisplay.listOfModeButtons)

        if nc.is_term_resized(CringeDisplay.screenSize[0], CringeDisplay.screenSize[1]):
            CringeDisplay.screen.clear()
            CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
            minSize = CringeDisplay.getRequieredSize()
            minW = CringeDisplay.screenSize[1] - minSize[0]
            minH = CringeDisplay.screenSize[0] - minSize[1]
            
            while minW < 0 or minH < 0:
                CringeDisplay.screenSize = CringeDisplay.screen.getmaxyx()
                minSize = CringeDisplay.getRequieredSize()
                minW = CringeDisplay.screenSize[1] - minSize[0]
                minH = CringeDisplay.screenSize[0] - minSize[1]

                CringeDisplay.screen.addch(0, 0, "")
                CringeDisplay.screen.refresh()

            CringeDisplay.resetWidgetsPosition()
            CringeWidgets.drawAllWidgetsIn(CringeDisplay.listOfAllWidgets)
            
        CringeDisplay.statusBar.updateText(f"W:{CringeDisplay.screenSize[1]}, H:{CringeDisplay.screenSize[0]}")
