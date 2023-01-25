import PySimpleGUI as sg

class MenuItem:
    def __init__(self,name:str,enabled:bool=True,key=None):
        self.name = name
        self.enabled = enabled
        self.key = key
        
    def __str__(self) -> str:
        return f"{'' if self.enabled else '!'}{self.name}{'::' if self.key else ''}{self.key}"

## Main Status Bar ##
statusBar = sg.StatusBar("test",
                         expand_y=True)
## Main Status Bar ##

## Main Menu Bar ##
saveBtn   = MenuItem("&Save",             enabled=False, key="menuSave")
undobtn   = MenuItem("&Undo",             enabled=False, key="undo")
redoBtn   = MenuItem("&Redo",             enabled=False, key="redo")
copyBtn   = MenuItem("&Copy",             enabled=False, key="copy")
cutBtn    = MenuItem("C&ut",              enabled=False, key="cut")
pasteBtn  = MenuItem("&Paste",            enabled=False, key="paste")
delBtn    = MenuItem("&Delete Selection", enabled=False, key="delete")
invSelBtn = MenuItem("&Invert Selection", enabled=False, key="invSel")

def menuBarDef():
    return  [["&File",[
                "&New::menuNew",
                "&Open::menuOpen",
                "---",
                str(saveBtn),
                "Save &As",
                "&Export",
                "---",
                "&Quit"
            ]],
             ["&Edit",[
                str(undobtn),
                str(redoBtn),
                "---",
                str(copyBtn),
                str(cutBtn),
                str(pasteBtn),
                "---",
                "Select &All::selectAll",
                str(invSelBtn),
                str(delBtn),
                "---",
                "&Preferences::menuPreferences"
            ]],
             ["&Help",[
                "&Help",
                "&Git",
                "&About"
            ]]]

menuBar = sg.Menu(menuBarDef())
## Main Menu Bar ##

right_click_menu = ["", ["Placeholder"]]