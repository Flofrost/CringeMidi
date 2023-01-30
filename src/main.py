#!/bin/python3
from __future__ import annotations
import curses as nc

import CringeMidi
from CringeMisc import *
import CringeWidgets

def main(screen:nc._CursesWindow):

    if nc.has_colors():
        nc.use_default_colors()
        nc.init_pair(1, 135, -1)

    nc.mousemask(-1)

    screen.nodelay(1)
    screen.timeout(50)
    
    modes = ["Normal", "Insert", "Visual", "Play"]
    mode = modes[0]
    i = 0
    screenSize = screen.getmaxyx()
    
    listOfAllInteractibleWidgets: CringeWidgets.InteractibleWidget = [
        CringeWidgets.ToggleButton(screen=screen,
                                   name=modes[0],
                                   position=[0,0],
                                   text=" Normal",
                                   style="bordered"),
        CringeWidgets.ToggleButton(screen=screen,
                                   name=modes[1],
                                   position=[10,0],
                                   text=" Insert",
                                   style="bordered"),
        CringeWidgets.ToggleButton(screen=screen,
                                   name=modes[2],
                                   position=[20,0],
                                   text="麗​ Visual",
                                   style="bordered"),
        CringeWidgets.ToggleButton(screen=screen,
                                   name=modes[3],
                                   position=[31,0],
                                   text="金​ Play",
                                   style="bordered"),
    ]

    statusBar = CringeWidgets.StatusBar(screen=screen,
                                        name="statusBar",
                                        justification="left",
                                        color=1)

    listOfAllWidgetsInDaProgram: CringeWidgets.Widget = [
        statusBar
    ] + listOfAllInteractibleWidgets

    while True:
        
        event = screen.getch()
        
        if event == nc.KEY_MOUSE:
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            
            for widget in listOfAllInteractibleWidgets:
                if widget.clicked(event, eventPosition):
                    pass

        if nc.is_term_resized(screenSize[0], screenSize[1]):
            screen.clear()
            screenSize = screen.getmaxyx()
            
            for widget in listOfAllWidgetsInDaProgram:
                widget.draw()
            
        i += 1
        statusBar.updateText(f"Counter = {i}")

if __name__ == "__main__":
    nc.wrapper(main)