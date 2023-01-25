import PySimpleGUI as sg

def exitConfirmWindow():
    sg.popup(title="Exiting CringeMidi",
             keep_on_top=True,
             custom_text=("&Yes","&No","&Cancel"))