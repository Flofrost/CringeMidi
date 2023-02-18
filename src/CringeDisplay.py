import curses as nc
from CringeEvents import *
import CringeGlobals
from CringeWidgets import *

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
        self.listeners = eventListeners if eventListeners else []

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
        listOfInteractibles = []
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
            color=nc.color_pair(CRINGE_COLOR_BLUE)
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
            color=nc.color_pair(CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        ),
        Expander(
            screen=screen
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
            color=nc.color_pair(CRINGE_COLOR_BLUE)
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
            color=nc.color_pair(CRINGE_COLOR_BLUE)
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
            color=nc.color_pair(CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=CringeGlobals.screen,
            size=2
        )
    ]
)

instrumentList = InstrumentList(
    screen=CringeGlobals.screen,
    name="instrumentList",
    position=[CringeGlobals.screen.getmaxyx()[1] - 20, 4]
)

statusBar = StatusBar(
    screen=CringeGlobals.screen,
    color=CRINGE_COLOR_PRPL
)
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

def normalKeyboardEvents(event: int):
    global instrumentList

    if  event == ord("i"):
        raiseEvent("modeUpdate", "insert")

    elif event == ord("u"):
        raiseEvent("undo")
    elif event == ord("r"):
        raiseEvent("redo")

    elif event == ord("N"):
        raiseEvent("addInstrument")
    elif event == ord("D"):
        raiseEvent("rmvInstrument")
    elif event == ord("J"):
        raiseEvent("dwnInstrument")
    elif event == ord("K"):
        raiseEvent("uppInstrument")
    elif event == ord("C"):
        raiseEvent("changeInstrument", "color")
    elif event == ord("V"):
        raiseEvent("changeInstrument", "visible")
    elif event == ord("T"):
        raiseEvent("changeInstrument", "type")
    elif event == ord("R"):
        raiseEvent("changeInstrument", "name")
    elif event == nc.KEY_DOWN:
        instrumentList.selectNext()
    elif event == nc.KEY_UP:
        instrumentList.selectNext(False)
    else:
        CringeGlobals.debugInfo = event

def normalPositionner():
    instrumentList.position = [CringeGlobals.screen.getmaxyx()[1] - 20, 5]
    modeList["normal"].getWidget("separatorLine").position = [CringeGlobals.screen.getmaxyx()[1] - 21, 3]
    modeList["normal"].getWidget("instrumentListToolbar").position = [CringeGlobals.screen.getmaxyx()[1] - 20, 4]

def onInstrumentListUpdate(instrumentList: InstrumentList):
    global rmvInstrumentBtn, uppInstrumentBtn, dwnInstrumentBtn

    rmvInstrumentBtn.enabled = True if len(instrumentList.instrumentList) > 1 else False
    uppInstrumentBtn.enabled = True if instrumentList.selectee > 0 else False
    dwnInstrumentBtn.enabled = True if instrumentList.selectee < len(instrumentList.instrumentList) - 1 else False
    
    rmvInstrumentBtn.draw()
    uppInstrumentBtn.draw()
    dwnInstrumentBtn.draw()
### Normal ###

### Insert ###
def insertKeyboardEvents(event: int):
    if event == 27:
        raiseEvent("modeUpdate", "normal")

def insertPositionner():
    pass
### Insert ###

### Settings ###
def helpKeyboardEvents(event: int):
    if event == 27:
       raiseEvent("modeUpdate", "normal")
        
def helpPositionner():
    pass
### Settings ###

### Help ###
def settingsKeyboardEvents(event: int):
    if event == 27:
        raiseEvent("modeUpdate", "normal")

def settingsPositionner():
    pass
### Help ###

modeList = {
    "normal" : Mode(
        keyboardEventHandler=normalKeyboardEvents,
        widgetPositionner=normalPositionner,
        eventListeners=[
            ["instrumentListUpdate", onInstrumentListUpdate],
            ["addInstrument", instrumentList.addInstrument],
            ["rmvInstrument", instrumentList.rmvInstrument],
            ["uppInstrument", instrumentList.uppInstrument],
            ["dwnInstrument", instrumentList.dwnInstrument],
            ["changeInstrument", instrumentList.changeInstrument]
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
            instrumentList,
        ]
    ),
    "insert" : Mode(
        keyboardEventHandler=insertKeyboardEvents,
        widgetPositionner=insertPositionner,
        widgets=[],
    ),
    "settings" : Mode(
        keyboardEventHandler=settingsKeyboardEvents,
        widgetPositionner=settingsPositionner,
        widgets=[],
    ),
    "help" : Mode(
        keyboardEventHandler=helpKeyboardEvents,
        widgetPositionner=helpPositionner,
        widgets=[
            Layout(
                screen=CringeGlobals.screen,
                name="helpToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=CringeGlobals.screen,
                        text=" "
                    ),
                    Button(
                        screen=CringeGlobals.screen,
                        name="prev",
                        text="<"
                    ),
                    Expander(screen=screen),
                    Text(
                        screen=CringeGlobals.screen,
                        name="sectionName"
                    ),
                    Expander(screen=screen),
                    Button(
                        screen=CringeGlobals.screen,
                        name="next",
                        text=">"
                    ),
                    Text(
                        screen=CringeGlobals.screen,
                        text=" "
                    )
                ]
            ),
            HLine(
                screen=CringeGlobals.screen,
                position=[0, 3],
                expand=True
            )
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

    redrawScreen()

def onScreenResized():
    global activeMode

    activeMode.widgetsPositionner()

def modeButtonsClickHandler(clickType, clickPosition):
    for button in mainToolbar.interactibles:
        button.clickHandler(clickType, clickPosition)
### Events Reactions ###

### Subscribtions ###
subscribe("modeUpdate", onModeUpdate)
subscribe("mouseEvent", modeButtonsClickHandler)
subscribe("screenResized", onScreenResized)
### Subscribtions ###

### Functions ###
def redrawScreen() -> None:
    # global activeMode
    screen.erase()

    mainToolbar.draw()
    HLine(
        CringeGlobals.screen,
        position=[0, 1],
        expand=True
    ).draw()
    
    activeMode.drawFunction()

def screenResizeCheckerandUpdater() -> list[int, int]:
    minW = screen.getmaxyx()[1] - max(mainToolbar.size[0], len("".join(statusBar.text)))
    minH = screen.getmaxyx()[0] - 15
    
    while minW < 0 or minH < 0:
        minW = screen.getmaxyx()[1] - max(mainToolbar.size[0], len("".join(statusBar.text))) - 2
        minH = screen.getmaxyx()[0] - 15 - 2

        screen.erase()
        screen.addch(0, 0, "")
        screen.refresh()

    raiseEvent("screenResized")
    redrawScreen()
    return screen.getmaxyx()
### Functions ###