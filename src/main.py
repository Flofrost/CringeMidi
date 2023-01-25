#!/bin/python3
from re import search
import PySimpleGUI as sg

import CringeWidgets
import CringeWindows

if __name__ == "__main__":
    
    sg.theme("DarkPurple1")

    test = sg.Text("",expand_x=True,expand_y=True)

    # ------ GUI Defintion ------ #
    layout = [
        [CringeWidgets.menuBar],
        [test],
        [CringeWidgets.statusBar]
    ]

    window = sg.Window("CringeMidi",
                       layout,
                       element_padding = (5,3),
                       resizable = True,
                       finalize=True)
    
    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        
        if search("::.+$",event):
            event = event.split("::")[1]

        if event in (sg.WIN_CLOSED,"Quit"):
            break
        
        CringeWidgets.saveBtn.enabled = not CringeWidgets.saveBtn.enabled
        CringeWidgets.menuBar.update(CringeWidgets.menuBarDef())
        
        test.update(event)

    window.close()