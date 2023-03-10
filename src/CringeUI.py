import curses as nc
import re

from CringeEvents import *
import CringeGlobals
import CringeDisplay
from CringeWidgets import *
import CringeGlobals

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
        subscribe("keyboardEvent", self.keyboardEventsHandler)
        subscribe("mouseEvent", self.handleMouseEvents)
        for listerner in self.listeners:
            subscribe(listerner[0], listerner[1])
        
    def unloadMode(self):
        unsubscribe("keyboardEvent", self.keyboardEventsHandler)
        unsubscribe("mouseEvent", self.handleMouseEvents)
        for listerner in self.listeners:
            unsubscribe(listerner[0], listerner[1])

    def drawFunction(self) -> None:
        for w in self.widgets:
            w.draw()

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
    screen=CringeDisplay.screen,
    name="mainToolbar",
    position=[0, 0],
    contents=[
        VLine(
            screen=CringeDisplay.screen,
            size=2
        ),
        Button(
            screen=CringeDisplay.screen,
            name="normal",
            eventToRaise="modeUpdate",
            text="󱣱 Normal",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeDisplay.screen,
            size=2
        ),
        Button(
            screen=CringeDisplay.screen,
            name="insert",
            eventToRaise="modeUpdate",
            text=" Insert",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeDisplay.screen,
            size=2
        ),
        Expander(
            screen=CringeDisplay.screen
        ),
        VLine(
            screen=CringeDisplay.screen,
            size=2
        ),
        Button(
            screen=CringeDisplay.screen,
            name="settings",
            eventToRaise="modeUpdate",
            text=" Settings",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeDisplay.screen,
            size=2
        ),
        Button(
            screen=CringeDisplay.screen,
            name="help",
            eventToRaise="modeUpdate",
            text=" Help",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeDisplay.screen,
            size=2
        ),
        Button(
            screen=CringeDisplay.screen,
            name="exit",
            eventToRaise="exit",
            text=" Exit",
            color=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeDisplay.screen,
            size=2
        )
    ]
)

project = Project(
    screen=CringeDisplay.screen,
    name="instrumentList",
    position=[CringeDisplay.screen.getmaxyx()[1] - 20, 4]
)

sheet =  Sheet(
    screen=CringeDisplay.screen,
    name="sheet",
    project=project,
    position=[0, 4],
)

statusBar = StatusBar(
    screen=CringeDisplay.screen,
    color=CringeGlobals.CRINGE_COLOR_PRPL
)

rewindList = list()
rewindIndex = 0
### Global ###

### Normal ###
saveBtn = Button(
    screen=CringeDisplay.screen,
    name="save",
    text="󰠘 ",
    eventToRaise="saveProject",
    enabled=False
)
undoBtn = Button(
    screen=CringeDisplay.screen,
    name="undo",
    text="󰕍 ",
    enabled=False
)
redoBtn = Button(
    screen=CringeDisplay.screen,
    name="redo",
    text="󰑏 ",
    enabled=False
)

addInstrumentBtn = Button(
                    screen=CringeDisplay.screen,
                    name="addInstrument",
                    text=" "
                )
rmvInstrumentBtn = Button(
                    screen=CringeDisplay.screen,
                    name="rmvInstrument",
                    text=" ",
                    enabled=False
                )
uppInstrumentBtn = Button(
                    screen=CringeDisplay.screen,
                    name="uppInstrument",
                    text=" ",
                    enabled=False
                )
dwnInstrumentBtn = Button(
                    screen=CringeDisplay.screen,
                    name="dwnInstrument",
                    text=" ",
                    enabled=False
                )

def normalKeyboardEvents(event: str):
    global project, sheet

    preserveCombo = False
    command = [""]

    if  event == "i": # Insert Mode
        raiseEvent("modeUpdate", "insert")
    elif event == "H": # Help Mode
        raiseEvent("modeUpdate", "help")
    elif event == ":": # Command Mode
        commandHandler()

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

    elif regexTest(r"^(\d+)?(?:J|SHIFT\+↓)$", CringeGlobals.commandCombo + event, command): # Select Next Intrument
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            project.selectNext()
    elif regexTest(r"^(\d+)?(?:K|SHIFT\+↑)$", CringeGlobals.commandCombo + event, command): # Select Next Intrument
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            project.selectNext(False)
    elif regexTest(r"^(\d+)?CTRL\+↓$", CringeGlobals.commandCombo + event, command): # Move Instrument Down
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            raiseEvent("dwnInstrument")
    elif regexTest(r"^(\d+)?CTRL\+↑$", CringeGlobals.commandCombo + event, command): # Move Instrument Up
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
        raiseEvent("instrumentListUpdate", project)
    elif re.findall(r"^mv$", CringeGlobals.commandCombo + event): # Toggle Instrument Visibility
        raiseEvent("changeInstrument", "visible")
        raiseEvent("instrumentListUpdate", project)
    elif re.findall(r"^mt$", CringeGlobals.commandCombo + event): # Change Instrument Type
        raiseEvent("changeInstrument", "type")
    elif re.findall(r"^mr$", CringeGlobals.commandCombo + event): # Change Instrument Name
        raiseEvent("changeInstrument", "name")
        
    elif regexTest(r"^(\d+)?(?:k|↑)$", CringeGlobals.commandCombo + event, command): # Pan Up
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            sheet.scrollV(True)
    elif regexTest(r"^(\d+)?(?:j|↓)$", CringeGlobals.commandCombo + event, command): # Pan Down
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            sheet.scrollV()
    elif regexTest(r"^(\d+)?(?:h|←)$", CringeGlobals.commandCombo + event, command): # Pan Left
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            sheet.scrollH(True)
    elif regexTest(r"^(\d+)?(?:l|→)$", CringeGlobals.commandCombo + event, command): # Pan Right
        count: str = command[0][0]
        count = max(int(count), 1) if count.isnumeric() else 1
        for i in range(count):
            sheet.scrollH()

    elif event == "Esc" and CringeGlobals.commandCombo:
        CringeGlobals.commandCombo = ""
    elif event in ("Esc", "Return") and CringeGlobals.scheduledSaveStateStatus:
        unschedule("saveState")
        raiseEvent("saveState")
    elif event == "Esc":
        CringeGlobals.commandCombo = ""
    elif not re.findall(r"Return|Backspace|CTRL|SHIFT", event): # Ignore some inputs if they're the first in the combo
        preserveCombo = True
        
    if preserveCombo:
        CringeGlobals.commandCombo += event
    else:
        CringeGlobals.commandCombo = ""

def normalPositionner():
    project.position = [CringeDisplay.screen.getmaxyx()[1] - 20, 5]
    sheet.resize([CringeDisplay.screen.getmaxyx()[1] - 20, CringeDisplay.screen.getmaxyx()[0] - 5])
    modeList["normal"].getWidget("separatorLine").position = [CringeDisplay.screen.getmaxyx()[1] - 21, 3]
    modeList["normal"].getWidget("instrumentListToolbar").position = [CringeDisplay.screen.getmaxyx()[1] - 20, 4]

def onInstrumentListUpdate(instrumentList: Project):
    global rmvInstrumentBtn, uppInstrumentBtn, dwnInstrumentBtn

    rmvInstrumentBtn.enabled = len(instrumentList.instrumentList) > 1
    uppInstrumentBtn.enabled = instrumentList.selectee > 0 
    dwnInstrumentBtn.enabled = instrumentList.selectee < len(instrumentList.instrumentList) - 1 
    
    rmvInstrumentBtn.draw()
    uppInstrumentBtn.draw()
    dwnInstrumentBtn.draw()
    
    sheet.draw()

def commandHandler():
    command = CringeDisplay.textInputPrompt(prompt="Command : ", attributes=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE))
    
    if command in ("w", "write", "save"):
        raiseEvent("saveProject")
    elif command in ("q", "quit", "exit"):
        raiseEvent("exit")
    elif command == "wq":
        raiseEvent("saveProject")
        raiseEvent("exit")
    elif command in ("debug", "log"):
        raiseEvent("modeUpdate", "debug")

def undoRedoBtnsUpdate(*_):
    global rewindIndex, rewindList
    
    undoBtn.enabled = rewindIndex + 1 < len(rewindList)
    undoBtn.draw()
    
    redoBtn.enabled = rewindIndex > 0
    redoBtn.draw()
    
    saveBtn.enabled = len(rewindList) > 1
    saveBtn.draw()
    CringeGlobals.projectSavedStatus = "" if len(rewindList) > 1 else "󱣫 "
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
    screen=CringeDisplay.screen,
    name="helpTextBody",
    text=CringeGlobals.helpContents[0][1],
    position=[1, 4],
    size=[CringeDisplay.screen.getmaxyx()[1] - 2, CringeDisplay.screen.getmaxyx()[0] - 7]
)
helpTextBody.pageIndex = 0

helpHeader = Text(
    screen=CringeDisplay.screen,
    name="sectionName"
)
helpHeader.changeText(f"{CringeGlobals.helpContents[helpTextBody.pageIndex][0]} {helpTextBody.pageIndex + 1}/{len(CringeGlobals.helpContents)}")

def helpKeyboardEvents(event: str):
    if event == "Esc":
       raiseEvent("modeUpdate", "normal")
       
    elif event == "←":
        raiseEvent("changePage", "prev")
    elif event == "→":
        raiseEvent("changePage", "next")
        
def helpPositionner():
    helpTextBody.resize([CringeDisplay.screen.getmaxyx()[1] - 2, CringeDisplay.screen.getmaxyx()[0] - 7])
    
def onHelpPageChange(next: Widget | str):
    global helpTextBody, helpHeader, activeMode
    
    if isinstance(next, Widget):
        next = next.name
        
    if next == "next":
        helpTextBody.pageIndex = (helpTextBody.pageIndex + 1) % len(CringeGlobals.helpContents)
    else:
        helpTextBody.pageIndex = (helpTextBody.pageIndex - 1) % len(CringeGlobals.helpContents)

    helpTextBody.changeText(CringeGlobals.helpContents[helpTextBody.pageIndex][1])
    helpHeader.changeText(f"{CringeGlobals.helpContents[helpTextBody.pageIndex][0]} {helpTextBody.pageIndex + 1}/{len(CringeGlobals.helpContents)}")
    activeMode.drawFunction()
### Help ###

### Debug ###
debugTextBody = LargeText(
    screen=CringeDisplay.screen,
    name="debugTextBody",
    text=CringeGlobals.debugContents[0][1],
    position=[1, 4],
    size=[CringeDisplay.screen.getmaxyx()[1] - 2, CringeDisplay.screen.getmaxyx()[0] - 7]
)
debugTextBody.pageIndex = 0

debugHeader = Text(
    screen=CringeDisplay.screen,
    name="sectionName"
)
debugHeader.changeText(f"{CringeGlobals.debugContents[debugTextBody.pageIndex][0]} {debugTextBody.pageIndex + 1}/{len(CringeGlobals.debugContents)}")

def debugKeyboardEvents(event: str):
    if event == "Esc":
       raiseEvent("modeUpdate", "normal")
       
    elif event == "←":
        raiseEvent("changePage", "prev")
    elif event == "→":
        raiseEvent("changePage", "next")
        
def debugPositionner():
    debugTextBody.resize([CringeDisplay.screen.getmaxyx()[1] - 2, CringeDisplay.screen.getmaxyx()[0] - 7])
    
def onDebugPageChange(next: Widget | str):
    global debugTextBody, debugHeader, activeMode
    
    if isinstance(next, Widget):
        next = next.name
        
    if next == "next":
        debugTextBody.pageIndex = (debugTextBody.pageIndex + 1) % len(CringeGlobals.debugContents)
    else:
        debugTextBody.pageIndex = (debugTextBody.pageIndex - 1) % len(CringeGlobals.debugContents)

    debugTextBody.changeText(CringeGlobals.debugContents[debugTextBody.pageIndex][1])
    debugHeader.changeText(f"{CringeGlobals.debugContents[debugTextBody.pageIndex][0]} {debugTextBody.pageIndex + 1}/{len(CringeGlobals.debugContents)}")
    activeMode.drawFunction()
### Debug ###

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
                screen=CringeDisplay.screen,
                name="normalToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                    saveBtn,
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                    undoBtn,
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                    redoBtn,
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                ]
            ),
            HLine(
                screen=CringeDisplay.screen,
                position=[0, 3],
                expand=True
            ),
            Layout(
                screen=CringeDisplay.screen,
                name="instrumentListToolbar",
                position=[0, 4],
                maxSize=20,
                contents=[
                    Expander(
                        screen=CringeDisplay.screen,
                        filler="⠀"
                    ),
                    addInstrumentBtn,
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                    rmvInstrumentBtn,
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀⠀"
                    ),
                    uppInstrumentBtn,
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                    dwnInstrumentBtn,
                    Expander(
                        screen=CringeDisplay.screen,
                        filler="⠀"
                    ),
                ]
            ),
            sheet,
            VLine(
                screen=CringeDisplay.screen,
                name="separatorLine",
                position=[CringeDisplay.screen.getmaxyx()[1] - 20 - 1, 3],
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
            ["changePage", onHelpPageChange]
        ],
        widgets=[
            Layout(
                screen=CringeDisplay.screen,
                name="helpToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                    Button(
                        screen=CringeDisplay.screen,
                        name="prev",
                        eventToRaise="changePage",
                        text=" "
                    ),
                    Expander(screen=CringeDisplay.screen),
                    helpHeader,
                    Expander(screen=CringeDisplay.screen),
                    Button(
                        screen=CringeDisplay.screen,
                        name="next",
                        eventToRaise="changePage",
                        text=" "
                    ),
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                ]
            ),
            HLine(
                screen=CringeDisplay.screen,
                position=[0, 3],
                expand=True
            ),
            helpTextBody
        ],
    ),
    "debug" : Mode(
        keyboardEventHandler=debugKeyboardEvents,
        widgetPositionner=debugPositionner,
        eventListeners=[
            ["changePage", onDebugPageChange]
        ],
        widgets=[
            Layout(
                screen=CringeDisplay.screen,
                name="debugToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                    Button(
                        screen=CringeDisplay.screen,
                        name="prev",
                        eventToRaise="changePage",
                        text=" "
                    ),
                    Expander(screen=CringeDisplay.screen),
                    debugHeader,
                    Expander(screen=CringeDisplay.screen),
                    Button(
                        screen=CringeDisplay.screen,
                        name="next",
                        eventToRaise="changePage",
                        text=" "
                    ),
                    Text(
                        screen=CringeDisplay.screen,
                        text="⠀"
                    ),
                ]
            ),
            HLine(
                screen=CringeDisplay.screen,
                position=[0, 3],
                expand=True
            ),
            debugTextBody
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

    raiseEvent("screenResized")

def onScreenResized():
    global activeMode

    activeMode.widgetsPositionner()
    redrawScreen()

def modeButtonsClickHandler(clickType, clickPosition):
    for button in mainToolbar.interactibles:
        button.clickHandler(clickType, clickPosition)

def onScheduleSaveState():
    CringeGlobals.scheduledSaveStateStatus = "󱫍 "
    schedule("saveState", onSaveState, 100)

def onSaveState():
    global rewindIndex, rewindList, project

    CringeGlobals.scheduledSaveStateStatus = ""

    state = project.save()

    if not rewindList or state != rewindList[rewindIndex]:
        if rewindIndex:
            rewindList = rewindList[rewindIndex:]
            rewindIndex = 0
        rewindList.insert(0, project.save())
        raiseEvent("rewindListUpdated")

def onUndo(*_):
    global rewindIndex, rewindList
    
    if CringeGlobals.scheduledSaveStateStatus:
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

def saveProject(*_):
    global project
    
    file = open(project.projectPath, "w")
    file.write(project.save(True))
    file.close()
    
    saveBtn.enabled = False
    saveBtn.draw()
    CringeGlobals.projectSavedStatus = "󱣫 "
    
def loadProject():
    global project

    file = open(project.projectPath, "r")
    project.load(file.read())
    file.close()

    saveBtn.enabled = False
    saveBtn.draw()
    CringeGlobals.projectSavedStatus = "󱣫 "

def redrawScreen() -> None:
    CringeDisplay.screen.erase()

    mainToolbar.draw()
    HLine(
        CringeDisplay.screen,
        position=[0, 1],
        expand=True
    ).draw()
    
    activeMode.drawFunction()
### Events Reactions ###

### Subscribtions ###
subscribe("modeUpdate", onModeUpdate)
subscribe("mouseEvent", modeButtonsClickHandler)
subscribe("screenResized", onScreenResized)
subscribe("scheduleSaveState", onScheduleSaveState)
subscribe("saveState", onSaveState)
subscribe("undo", onUndo)
subscribe("redo", onRedo)
subscribe("saveProject", saveProject)
### Subscribtions ###