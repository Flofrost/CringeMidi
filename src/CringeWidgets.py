import os
import PySimpleGUI as sg
from CringeMidi import *

assetsPath = os.path.abspath(".") + os.sep + "assets" + os.sep 

class MenuItem:
    def __init__(self,name:str,enabled:bool=True,key=""):
        self.name = name
        self.enabled = enabled
        self.key = key
        
    def __str__(self) -> str:
        return f"{'' if self.enabled else '!'}{self.name}{'::' if self.key else ''}{self.key}"

## Main Status Bar ##
statusBar = sg.StatusBar("test",
                         expand_x=True,
                         size=150,
                         relief=sg.RELIEF_FLAT)
## Main Status Bar ##

## Main Menu Bar ##
saveMenuBtn   = MenuItem("&Save",             enabled=False, key="save")
undoMenuBtn   = MenuItem("&Undo",             enabled=False, key="undo")
redoMenuBtn   = MenuItem("&Redo",             enabled=False, key="redo")
copyMenuBtn   = MenuItem("&Copy",             enabled=False, key="copy")
cutMenuBtn    = MenuItem("C&ut",              enabled=False, key="cut")
pasteMenuBtn  = MenuItem("&Paste",            enabled=False, key="paste")
delMenuBtn    = MenuItem("&Delete Selection", enabled=False, key="delete")
invSelMenuBtn = MenuItem("&Invert Selection", enabled=False, key="invSel")
projectBtn    = MenuItem("&Project",          enabled=False)

def menuBarDef():
    return  [["&File",[
                "&New::new",
                "&Open::open",
                "---",
                str(saveMenuBtn),
                "Save &As::saveAs",
                "&Export Audio::export",
                "---",
                "&Quit"
            ]],
             ["&Edit",[
                str(undoMenuBtn),
                str(redoMenuBtn),
                "---",
                str(copyMenuBtn),
                str(cutMenuBtn),
                str(pasteMenuBtn),
                "---",
                "Select &All::selectAll",
                str(invSelMenuBtn),
                str(delMenuBtn),
                "---",
                "&Preferences::menuPreferences"
            ]],
             [str(projectBtn),[
                "Project &Settings::projectSettings",
                "&Generate Code::generateCode"
             ]],
             ["&Help",[
                "&Help::help",
                "&Git::browseGit",
                "&About::about"
            ]]]

menuBar = sg.Menu(menuBarDef())
## Main Menu Bar ##

### Main Tool Bar ###
undoToolBtn = sg.Button(image_source=assetsPath + "undo.png", key="undo", tooltip="Undo")
redoToolBtn = sg.Button(image_source=assetsPath + "redo.png", key="redo", tooltip="Redo")

def toolBarDef():
    return  [[
        undoToolBtn,
        redoToolBtn
    ]]

toolBar = sg.Frame("",toolBarDef(),
                   expand_x=True)
### Main Tool Bar ###

### Instrument List ###
addInstrumentBtn = sg.Button("+", key="addInstrument", tooltip="Add Instrument")
rmvInstrumentBtn = sg.Button("-", key="rmvInstrument", tooltip="Remove Instrument", disabled=True)

instrumentList = [Instrument("test")]

# def instrumentsListWidgetDef(instrumentList:list=[]):
#     return [[
#         addInstrumentBtn,
#         rmvInstrumentBtn
#     ]] + [[ins.frame] for ins in instrumentList]

instrumentListWidget = sg.Listbox(instrumentList,
                                  expand_y=True,
                                  enable_events=True)
### Instrument List ###
