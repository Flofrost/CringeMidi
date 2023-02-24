import curses as nc
import curses.ascii as ac
import re

from CringeEvents import *
import CringeGlobals
from CringeWidgets import *
import CringeDocs

kbKeys = {
    nc.KEY_LEFT : "←",
    nc.KEY_RIGHT : "→",
    nc.KEY_UP : "↑",
    nc.KEY_DOWN : "↓",
    546 : "CTRL+←",
    561 : "CTRL+→",
    567 : "CTRL+↑",
    526 : "CTRL+↓",
    337 : "SHIFT+↑",
    336 : "SHIFT+↓",
    402 : "SHIFT+→",
    393 : "SHIFT+←",
    
    10 : "Return",
    27 : "Esc",
}

### Mode Manager Class ###
class Mode():
    
    def __init__(
            self,
            widgets: list[Widget] = None,
            keyboardEventHandler = None,
            widgetPositionner = None,
            eventListeners: list = None
        ) -> None:
        
        self.widgets  = widgets
        self.keyboardEventsHandler = keyboardEventHandler
        self.widgetsPositionner = widgetPositionner
        self.listeners = eventListeners if eventListeners else list()

    def loadMode(self):
        subscribe("keyboardEvent", self.handleKeyboardEvents)
        subscribe("mouseEvent", self.handleMouseEvents)
        for listerner in self.listeners:
            subscribe(listerner[0], listerner[1])
        
    def unloadMode(self):
        unsubscribe("keyboardEvent", self.handleKeyboardEvents)
        unsubscribe("mouseEvent", self.handleMouseEvents)
        for listerner in self.listeners:
            unsubscribe(listerner[0], listerner[1])

    def drawFunction(self) -> None:
        for w in self.widgets:
            w.draw()
    
    def handleKeyboardEvents(self, event: int) -> None:
        global kbKeys
        if ac.isprint(event):
            self.keyboardEventsHandler(chr(event))
        elif event in kbKeys:
            self.keyboardEventsHandler(kbKeys[event])
        else:
            CringeGlobals.debugInfo = event

    def handleMouseEvents(self, event: int, eventPosition: list[int, int]) -> None:
        for w in self.interactibles:
            w.clickHandler(event, eventPosition)
            
    def getWidget(self, name: str) -> Widget:
        for w in self.widgets:
            if w.name == name:
                return w
        raise Exception(f"No widget with name {name}")
        
    @property
    def interactibles(self) -> list[InteractibleWidget]:
        listOfInteractibles = list()
        for w in self.widgets:
            if isinstance(w, Layout):
                listOfInteractibles += w.interactibles
            elif isinstance(w, InteractibleWidget):
                listOfInteractibles.append(w)
        return listOfInteractibles
### Mode Manager Class ###

### Global ###
mainToolbar = Layout(
    screen=CringeGlobals.screen,
    name="mainToolbar",
    position=[0, 0],
    contents=[
        VLine(
            screen=CringeGlobals.screen,
            size=2
        ),
        Button(
            screen=CringeGlobals.screen,
            name="normal",
            eventToRaise="modeUpdate",
            text="󱣱 Normal",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        ),
        Button(
            screen=CringeGlobals.screen,
            name="insert",
            eventToRaise="modeUpdate",
            text=" Insert",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        ),
        Expander(
            screen=CringeGlobals.screen
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        ),
        Button(
            screen=CringeGlobals.screen,
            name="settings",
            eventToRaise="modeUpdate",
            text=" Settings",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        ),
        Button(
            screen=CringeGlobals.screen,
            name="help",
            eventToRaise="modeUpdate",
            text=" Help",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        ),
        Button(
            screen=CringeGlobals.screen,
            name="exit",
            eventToRaise="exit",
            text=" Exit",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        )
    ]
)

project = Project(
    screen=CringeGlobals.screen,
    name="instrumentList",
    position=[CringeGlobals.screen.getmaxyx()[1] - 20, 4]
)

statusBar = StatusBar(
    screen=CringeGlobals.screen,
    color=CringeGlobals.CRINGE_COLOR_PRPL
)

rewindList = list()
rewindIndex = 0
### Global ###

### Normal ###
undoBtn = Button(
    screen=CringeGlobals.screen,
    name="undo",
    text="󰕍 ",
    enabled=False
)
redoBtn = Button(
    screen=CringeGlobals.screen,
    name="redo",
    text="󰑏 ",
    enabled=False
)

addInstrumentBtn = Button(
                    screen=CringeGlobals.screen,
                    name="addInstrument",
                    text=" "
                )
rmvInstrumentBtn = Button(
                    screen=CringeGlobals.screen,
                    name="rmvInstrument",
                    text=" ",
                    enabled=False
                )
uppInstrumentBtn = Button(
                    screen=CringeGlobals.screen,
                    name="uppInstrument",
                    text=" ",
                    enabled=False
                )
dwnInstrumentBtn = Button(
                    screen=CringeGlobals.screen,
                    name="dwnInstrument",
                    text=" ",
                    enabled=False
                )

def normalKeyboardEvents(event: str):
    global project

    preserveCombo = False
    command = [""]

    if  event == "i": # Insert Mode
        raiseEvent("modeUpdate", "insert")
    elif event == "H": # Help Mode
        raiseEvent("modeUpdate", "help")

    elif regexTest(r"^(\d+)?u$", CringeGlobals.commandCombo + event, command): # Undo
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            raiseEvent("undo")
    elif regexTest(r"^(\d+)?r$", CringeGlobals.commandCombo + event, command): # Redo
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            raiseEvent("redo")

    elif regexTest(r"^(\d+)?(?:j|↓)$", CringeGlobals.commandCombo + event, command): # Select Next Intrument
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            project.selectNext()
    elif regexTest(r"^(\d+)?(?:k|↑)$", CringeGlobals.commandCombo + event, command): # Select Next Intrument
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            project.selectNext(False)
    elif regexTest(r"^(\d+)?(?:J|SHIFT\+↓)$", CringeGlobals.commandCombo + event, command): # Move Instrument Down
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            raiseEvent("dwnInstrument")
    elif regexTest(r"^(\d+)?(?:K|SHIFT\+↑)$", CringeGlobals.commandCombo + event, command): # Move Instrument Up
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            raiseEvent("uppInstrument")
    elif regexTest(r"^(\d+)?ma$", CringeGlobals.commandCombo + event, command): # Add Instrument
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            raiseEvent("addInstrument")
    elif regexTest(r"^(\d+)?md$", CringeGlobals.commandCombo + event, command): # Remove Instrument
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            raiseEvent("rmvInstrument")
        
    elif re.findall(r"^mc$", CringeGlobals.commandCombo + event): # Change Instrument Color
        raiseEvent("changeInstrument", "color")
    elif re.findall(r"^mv$", CringeGlobals.commandCombo + event): # Toggle Instrument Visibility
        raiseEvent("changeInstrument", "visible")
    elif re.findall(r"^mt$", CringeGlobals.commandCombo + event): # Change Instrument Type
        raiseEvent("changeInstrument", "type")
    elif re.findall(r"^mr$", CringeGlobals.commandCombo + event): # Change Instrument Name
        raiseEvent("changeInstrument", "name")
        
    elif event == "Esc":
        CringeGlobals.commandCombo = ""
    else:
        preserveCombo = True
        
    if preserveCombo:
        CringeGlobals.commandCombo += event
    else:
        CringeGlobals.commandCombo = ""

def normalPositionner():
    project.position = [CringeGlobals.screen.getmaxyx()[1] - 20, 5]
    modeList["normal"].getWidget("separatorLine").position = [CringeGlobals.screen.getmaxyx()[1] - 21, 3]
    modeList["normal"].getWidget("instrumentListToolbar").position = [CringeGlobals.screen.getmaxyx()[1] - 20, 4]

def onInstrumentListUpdate(instrumentList: Project):
    global rmvInstrumentBtn, uppInstrumentBtn, dwnInstrumentBtn

    rmvInstrumentBtn.enabled = len(instrumentList.instrumentList) > 1
    uppInstrumentBtn.enabled = instrumentList.selectee > 0 
    dwnInstrumentBtn.enabled = instrumentList.selectee < len(instrumentList.instrumentList) - 1 
    
    rmvInstrumentBtn.draw()
    uppInstrumentBtn.draw()
    dwnInstrumentBtn.draw()

def undoRedoBtnsUpdate(*_):
    global rewindIndex, rewindList
    
    undoBtn.enabled = rewindIndex + 1 < len(rewindList)
    undoBtn.draw()
    
    redoBtn.enabled = rewindIndex > 0
    redoBtn.draw()
### Normal ###

### Insert ###
def insertKeyboardEvents(event: str):
    if event == "Esc":
        raiseEvent("modeUpdate", "normal")
        raiseEvent("saveState")

def insertPositionner():
    pass
### Insert ###

### Settings ###
def settingsKeyboardEvents(event: str):
    if event == "Esc":
        raiseEvent("modeUpdate", "normal")

def settingsPositionner():
    pass
### Settings ###

### Help ###
helpTextBody = LargeText(
    screen=CringeGlobals.screen,
    name="helpTextBody",
    text=CringeDocs.helpContents[0][1],
    position=[1, 4],
    size=[CringeGlobals.screen.getmaxyx()[1] - 2, CringeGlobals.screen.getmaxyx()[0] - 7]
)
helpTextBody.pageIndex = 0

helpHeader = Text(
    screen=CringeGlobals.screen,
    name="sectionName"
)
helpHeader.changeText(f"{CringeDocs.helpContents[helpTextBody.pageIndex][0]} {helpTextBody.pageIndex + 1}/{len(CringeDocs.helpContents)}")

def helpKeyboardEvents(event: str):
    if event == "Esc":
       raiseEvent("modeUpdate", "normal")
       
    elif event == "←":
        raiseEvent("changeHelpPage", "prev")
    elif event == "→":
        raiseEvent("changeHelpPage", "next")
        
def helpPositionner():
    helpTextBody.resize([CringeGlobals.screen.getmaxyx()[1] - 2, CringeGlobals.screen.getmaxyx()[0] - 7])
    
def onPageChange(next: Widget | str):
    global helpTextBody, helpHeader, activeMode
    
    if isinstance(next, Widget):
        next = next.name
        
    if next == "next":
        helpTextBody.pageIndex = (helpTextBody.pageIndex + 1) % len(CringeDocs.helpContents)
    else:
        helpTextBody.pageIndex = (helpTextBody.pageIndex - 1) % len(CringeDocs.helpContents)

    helpTextBody.changeText(CringeDocs.helpContents[helpTextBody.pageIndex][1])
    helpHeader.changeText(f"{CringeDocs.helpContents[helpTextBody.pageIndex][0]} {helpTextBody.pageIndex + 1}/{len(CringeDocs.helpContents)}")
    activeMode.drawFunction()
### Help ###

modeList = {
    "normal" : Mode(
        keyboardEventHandler=normalKeyboardEvents,
        widgetPositionner=normalPositionner,
        eventListeners=[
            ["instrumentListUpdate", onInstrumentListUpdate],
            ["addInstrument", project.addInstrument],
            ["rmvInstrument", project.rmvInstrument],
            ["uppInstrument", project.uppInstrument],
            ["dwnInstrument", project.dwnInstrument],
            ["changeInstrument", project.changeInstrument],
            ["undo", undoRedoBtnsUpdate],
            ["redo", undoRedoBtnsUpdate],
            ["rewindListUpdated", undoRedoBtnsUpdate],
        ],
        widgets=[
            Layout(
                screen=CringeGlobals.screen,
                name="normalToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀"
                    ),
                    undoBtn,
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀"
                    ),
                    redoBtn,
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀"
                    ),
                ]
            ),
            HLine(
                screen=CringeGlobals.screen,
                position=[0, 3],
                expand=True
            ),
            Layout(
                screen=CringeGlobals.screen,
                name="instrumentListToolbar",
                position=[0, 4],
                maxSize=20,
                contents=[
                    Expander(
                        screen=CringeGlobals.screen,
                        filler="⠀"
                    ),
                    addInstrumentBtn,
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀"
                    ),
                    rmvInstrumentBtn,
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀⠀"
                    ),
                    uppInstrumentBtn,
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀"
                    ),
                    dwnInstrumentBtn,
                    Expander(
                        screen=CringeGlobals.screen,
                        filler="⠀"
                    ),
                ]
            ),
            VLine(
                screen=CringeGlobals.screen,
                name="separatorLine",
                position=[CringeGlobals.screen.getmaxyx()[1] - 20 - 1, 3],
                expand=True
            ),
            project,
        ]
    ),
    "insert" : Mode(
        keyboardEventHandler=insertKeyboardEvents,
        widgetPositionner=insertPositionner,
        widgets=list(),
    ),
    "settings" : Mode(
        keyboardEventHandler=settingsKeyboardEvents,
        widgetPositionner=settingsPositionner,
        widgets=list(),
    ),
    "help" : Mode(
        keyboardEventHandler=helpKeyboardEvents,
        widgetPositionner=helpPositionner,
        eventListeners=[
            ["changeHelpPage", onPageChange]
        ],
        widgets=[
            Layout(
                screen=CringeGlobals.screen,
                name="helpToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀"
                    ),
                    Button(
                        screen=CringeGlobals.screen,
                        name="prev",
                        eventToRaise="changeHelpPage",
                        text=" "
                    ),
                    Expander(screen=CringeGlobals.screen),
                    helpHeader,
                    Expander(screen=CringeGlobals.screen),
                    Button(
                        screen=CringeGlobals.screen,
                        name="next",
                        eventToRaise="changeHelpPage",
                        text=" "
                    ),
                    Text(
                        screen=CringeGlobals.screen,
                        text="⠀"
                    ),
                ]
            ),
            HLine(
                screen=CringeGlobals.screen,
                position=[0, 3],
                expand=True
            ),
            helpTextBody
        ],
    )
}

activeMode: Mode = modeList["normal"]
activeMode.loadMode()

### Events Reactions ###
def onModeUpdate(newMode: str | Widget):
    global activeMode, modeList

    if isinstance(newMode, Widget):
        newMode = newMode.name
    for modeButton in mainToolbar.interactibles:
        if modeButton.name == newMode:
            modeButton.color = modeButton.color | nc.A_REVERSE
        else:
            modeButton.color = modeButton.color & ~(nc.A_REVERSE)
    
    activeMode.unloadMode()
    activeMode = modeList[newMode]
    activeMode.loadMode()

    raiseEvent("CringeGlobals.screenResized")
    redrawScreen()

def onScreenResized():
    global activeMode

    activeMode.widgetsPositionner()

def modeButtonsClickHandler(clickType, clickPosition):
    for button in mainToolbar.interactibles:
        button.clickHandler(clickType, clickPosition)

def onScheduleSaveState():
    CringeGlobals.saveStateStatus = "󱫍 "
    schedule("saveState", onSaveState, 100)

def onSaveState():
    global rewindIndex, rewindList

    CringeGlobals.saveStateStatus = ""

    state = project.save()

    if not rewindList or state != rewindList[rewindIndex]:
        if rewindIndex:
            rewindList = rewindList[rewindIndex:]
            rewindIndex = 0
        rewindList.insert(0, project.save())
        raiseEvent("rewindListUpdated")

def onUndo(*_):
    global rewindIndex, rewindList
    
    if CringeGlobals.saveStateStatus:
        raiseEvent("saveState")

    if rewindIndex + 1 < len(rewindList):
        rewindIndex += 1
        project.load(rewindList[rewindIndex])
        redrawScreen()

def onRedo(*_):
    global rewindIndex, rewindList
    
    if rewindIndex > 0:
        rewindIndex -= 1
        project.load(rewindList[rewindIndex])
        redrawScreen()
### Events Reactions ###

### Subscribtions ###
subscribe("modeUpdate", onModeUpdate)
subscribe("mouseEvent", modeButtonsClickHandler)
subscribe("screenResized", onScreenResized)
subscribe("scheduleSaveState", onScheduleSaveState)
subscribe("saveState", onSaveState)
subscribe("undo", onUndo)
subscribe("redo", onRedo)
### Subscribtions ###

### Functions ###
def redrawScreen() -> None:
    CringeGlobals.screen.erase()

    mainToolbar.draw()
    HLine(
        CringeGlobals.screen,
        position=[0, 1],
        expand=True
    ).draw()
    
    activeMode.drawFunction()

def screenResizeCheckerandUpdater() -> list[int, int]:
    minW = CringeGlobals.screen.getmaxyx()[1] - max(mainToolbar.size[0], len("".join(statusBar.text)))
    minH = CringeGlobals.screen.getmaxyx()[0] - 15
    
    while minW < 0 or minH < 0:
        minW = CringeGlobals.screen.getmaxyx()[1] - max(mainToolbar.size[0], len("".join(statusBar.text))) - 2
        minH = CringeGlobals.screen.getmaxyx()[0] - 15 - 2

        CringeGlobals.screen.erase()
        CringeGlobals.screen.addch(0, 0, "")
        CringeGlobals.screen.refresh()

    raiseEvent("screenResized")
    redrawScreen()
    return CringeGlobals.screen.getmaxyx()
### Functions ###