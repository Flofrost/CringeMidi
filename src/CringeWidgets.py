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
saveMenuBtn   = MenuItem("&Save",             enabled=False, key="save")
undoMenuBtn   = MenuItem("&Undo",             enabled=False, key="undo")
redoMenuBtn   = MenuItem("&Redo",             enabled=False, key="redo")
copyMenuBtn   = MenuItem("&Copy",             enabled=False, key="copy")
cutMenuBtn    = MenuItem("C&ut",              enabled=False, key="cut")
pasteMenuBtn  = MenuItem("&Paste",            enabled=False, key="paste")
delMenuBtn    = MenuItem("&Delete Selection", enabled=False, key="delete")
invSelMenuBtn = MenuItem("&Invert Selection", enabled=False, key="invSel")

def menuBarDef():
    return  [["&File",[
                "&New::new",
                "&Open::open",
                "---",
                str(saveMenuBtn),
                "Save &As::saveAs",
                "&Export::export",
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
             ["&Help",[
                "&Help::help",
                "&Git::browseGit",
                "&About::about"
            ]]]

menuBar = sg.Menu(menuBarDef())
## Main Menu Bar ##

### Main Tool Bar ###
undoToolBtn = sg.Button(image_filename="../assets/undo.png", key="undo")
redoToolBtn = sg.Button(image_filename="../assets/redo.png", key="redo")

def toolBarDef():
    return  [[
        undoToolBtn,
        redoToolBtn
    ]]

toolBar = sg.Frame("",toolBarDef(),
                    expand_x=True)
### Main Tool Bar ###
