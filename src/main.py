#!/bin/python3
from __future__ import annotations
import curses as nc
from tkinter import Button

import CringeMidi
from CringeMisc import *
import CringeWidgets

def main(screen:nc._CursesWindow):

    if nc.has_colors():
        nc.use_default_colors()
    nc.mousemask(-1)

    screen.nodelay(1)

    delay = 1000
    mode = "normal"
    screenSize = screen.getmaxyx()
    
    statusBar = CringeWidgets.StatusBar(screen=screen,
                                        text="Testing...")
    
    statusBar.draw()

    while True:
        
        event = screen.getch()
        
        if event == nc.KEY_MOUSE:
            event = nc.getmouse()
            eventPosition = event[1:3]
            event = event[4]
            
            if event == nc.BUTTON1_TRIPLE_CLICKED:
                return

        if nc.is_term_resized(screenSize[0], screenSize[1]):
            screenSize = screen.getmaxyx()
            statusBar.draw()

        nc.napms(delay)

if __name__ == "__main__":
    nc.wrapper(main)