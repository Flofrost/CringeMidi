#!/bin/python3
import PySimpleGUI as sg
import CringeMenus

if __name__ == "__main__":

    sg.theme("DarkPurple6")

    # ------ GUI Defintion ------ #
    layout = [
        [sg.Menu(CringeMenus.menuBar, tearoff=False, pad=(200, 1))],
        [sg.Text('Right click me for a right click menu example')],
        [sg.Output(size=(60, 20))],
        [sg.ButtonMenu('ButtonMenu',  CringeMenus.right_click_menu, key='-BMENU-'), sg.Button('Plain Button')],
    ]

    window = sg.Window("Windows-like program",
                       layout,
                       default_element_size=(12, 1),
                       default_button_element_size=(12, 1),
                       right_click_menu=CringeMenus.right_click_menu)

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED,"Quit"):
            break

        # ------ Process menu choices ------ #
        # if event == 'About...':
        #     window.disappear()
        #     sg.popup('About this program', 'Version 1.0',
        #              'PySimpleGUI Version', sg.version,  grab_anywhere=True)
        #     window.reappear()
        # elif event == 'Open':
        #     filename = sg.popup_get_file('file to open', no_window=True)
        #     print(filename)
        # elif event == 'Properties':
        #     pass

    window.close()