#!/bin/python3
from re import search,Match
import PySimpleGUI as sg

import CringeWidgets
import CringeWindows

if __name__ == "__main__":
    
    ### Global Parameters ###

    sg.theme("DarkPurple1")


    ### GUI Setup ###
    layout = [
        [CringeWidgets.menuBar],
        [CringeWidgets.toolBar],
        [CringeWidgets.instrumentList, sg.Frame("",[[]])],
        [CringeWidgets.statusBar]
    ]

    window = sg.Window("CringeMidi",
                       layout,
                       element_padding = (5,3),
                       resizable = True,
                       finalize=True)
    
    ### Main Loop ###
    while True:
        event, values = window.read() # Reading events from window
        CringeWidgets.dada.bind("<Button-1>", sg.popup)
        
        if isinstance(event, str) and search("::.+$",event): # If event has a special key, extract the key from it
            event = event.split("::")[1]
            
        if event in (sg.WIN_CLOSED,"Quit"):
            if CringeWindows.exitProtocol():
                break

        CringeWidgets.menuBar.update(CringeWidgets.menuBarDef())
        CringeWidgets.instrumentList.update(CringeWidgets.instrumentsListBarDef())
        
        CringeWidgets.statusBar.update(event)

    window.close()