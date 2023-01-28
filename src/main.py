#!/bin/python3
from re import search
import PySimpleGUI as sg

import CringeMidi
import CringeMisc
import CringeWidgets
import CringeWindows

if __name__ == "__main__":
    
    ### Global Parameters ###

    sg.theme("DarkPurple1")


    ### GUI Setup ###
    layout = [
        [CringeWidgets.menuBar],
        [CringeWidgets.toolBar],
        [sg.Frame("Instruments",[[CringeWidgets.addInstrumentBtn, CringeWidgets.rmvInstrumentBtn], [CringeWidgets.instrumentListWidget]], expand_y=True), sg.Frame("",[[]])],
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
        
        if isinstance(event, str) and search("::.+$",event): # If event has a special key, extract the key from it
            event = event.split("::")[1]
            
        if event == "addInstrument":
            pass
        elif event in (sg.WIN_CLOSED,"Quit"):
            if CringeWindows.exitProtocol():
                break

        CringeWidgets.menuBar.update(CringeWidgets.menuBarDef())
        CringeWidgets.statusBar.update(event)

    window.close()