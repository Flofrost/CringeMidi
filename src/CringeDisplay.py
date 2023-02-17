import curses as nc
from CringeEvents import *
import CringeGlobals
from CringeWidgets import *

### Global ###
mainToolbar = Layout(
    screen=screen,
    name="mainToolbar",
    position=[0, 0],
    contents=[
        VLine(
            screen=screen,
            size=2
        ),
        Button(
            screen=screen,
            name="normal",
            eventToRaise="modeUpdate",
            text="󱣱 Normal",
            color=nc.color_pair(CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=screen,
            size=2
        ),
        Button(
            screen=screen,
            name="insert",
            eventToRaise="modeUpdate",
            text=" Insert",
            color=nc.color_pair(CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=screen,
            size=2
        ),
        Expander(
            screen=screen
        ),
        VLine(
            screen=screen,
            size=2
        ),
        Button(
            screen=screen,
            name="settings",
            eventToRaise="modeUpdate",
            text=" Settings",
            color=nc.color_pair(CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=screen,
            size=2
        ),
        Button(
            screen=screen,
            name="help",
            eventToRaise="modeUpdate",
            text=" Help",
            color=nc.color_pair(CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=screen,
            size=2
        ),
        Button(
            screen=screen,
            name="exit",
            eventToRaise="exit",
            text=" Exit",
            color=nc.color_pair(CRINGE_COLOR_BLUE)
        ),
        VLine(
            screen=screen,
            size=2
        )
    ]
)

instrumentList = InstrumentList(
    screen=screen,
    name="instrumentList",
    position=[0, 4]
)

statusBar = StatusBar(
    screen=screen,
    color=CRINGE_COLOR_PRPL
)
### Global ###

### Mode Manager Class ###
class Mode():
    
    def __init__(
            self,
            widgets: list[Widget] = None,
            keyboardEventHandler = None,
            eventListeners: list = None
        ) -> None:
        
        self.widgets  = widgets
        self.keyboardEventsHandler = keyboardEventHandler
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

### Normal ###
placeholder = Button(
    screen=screen,
    name="placeholder",
    text=" ",
    # enabled=False
)

addInstrumentBtn = Button(
                    screen=screen,
                    name="addInstrument",
                    text=" "
                )
rmvInstrumentBtn = Button(
                    screen=screen,
                    name="rmvInstrument",
                    text=" ",
                    enabled=False
                )
uppInstrumentBtn = Button(
                    screen=screen,
                    name="uppInstrument",
                    text=" ",
                    enabled=False
                )
dwnInstrumentBtn = Button(
                    screen=screen,
                    name="dwnInstrument",
                    text=" ",
                    enabled=False
                )

def normalKeyboardEvents(event: int):
    if  event == ord("i"):
        raiseEvent("modeUpdate", "insert")

    elif event == ord("u"):
        raiseEvent("undo")

    # elif event == ord("n"):
    #     CringeGlobals.sheet.addInstrument()
    # elif event == ord("N"):
    #     if len(CringeGlobals.sheet.instrumentList) > 1:
    #         CringeGlobals.sheet.rmvInstrument()
    # elif event == ord("J"):
    #     CringeGlobals.sheet.move(False)
    # elif event == ord("K"):
    #     CringeGlobals.sheet.move()
    # elif event == ord("C"):
    #     CringeGlobals.sheet.selectedInstrument.changeColor()
    #     CringeGlobals.sheet.draw()
    # elif event == ord("V"):
    #     CringeGlobals.sheet.selectedInstrument.toggleVisible()
    #     CringeGlobals.sheet.draw()
    # elif event == ord("T"):
    #     CringeGlobals.sheet.selectedInstrument.changeType()
    #     CringeGlobals.sheet.draw()
    # elif event == ord("L"):
    #     CringeGlobals.sheet.selectedInstrument.changeName()
    #     CringeGlobals.sheet.draw()
    # elif event == kbKeys["SHIFT+DOWN"]:
    #     CringeGlobals.sheet.selectNext()
    # elif event == kbKeys["SHIFT+UP"]:
    #     CringeGlobals.sheet.selectNext(next=False)
            
    else:
        CringeGlobals.debugInfo = event

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
### Insert ###

### Settings ###
def helpKeyboardEvents(event: int):
    if event == 27:
        raiseEvent("modeUpdate", "normal")
### Settings ###

### Help ###
def settingsKeyboardEvents(event: int):
    if event == 27:
        raiseEvent("modeUpdate", "normal")
### Help ###

modeList = {
    "normal" : Mode(
        keyboardEventHandler=normalKeyboardEvents,
        eventListeners=[
            ["instrumentListUpdate", onInstrumentListUpdate],
            ["addInstrument", instrumentList.addInstrument],
            ["rmvInstrument", instrumentList.rmvInstrument],
            ["uppInstrument", instrumentList.uppInstrument],
            ["dwnInstrument", instrumentList.dwnInstrument],
        ],
        widgets=[
            Layout(
                screen=screen,
                name="normalToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=screen,
                        text="⠀"
                    ),
                    placeholder,
                    Text(
                        screen=screen,
                        text="⠀"
                    ),
                ]
            ),
            HLine(
                screen=screen,
                position=[0, 3],
                expand=True
            ),
            Layout(
                screen=screen,
                name="instrumentListToolbar",
                position=[0, 4],
                maxSize=20,
                contents=[
                    Expander(
                        screen=screen,
                        filler="⠀"
                    ),
                    addInstrumentBtn,
                    Text(
                        screen=screen,
                        text="⠀"
                    ),
                    rmvInstrumentBtn,
                    Text(
                        screen=screen,
                        text="⠀⠀"
                    ),
                    uppInstrumentBtn,
                    Text(
                        screen=screen,
                        text="⠀"
                    ),
                    dwnInstrumentBtn,
                    Expander(
                        screen=screen,
                        filler="⠀"
                    ),
                ]
            ),
            VLine(
                screen=screen,
                position=[20, 3],
                expand=True
            ),
            instrumentList,
        ]
    ),
    "insert" : Mode(
        keyboardEventHandler=insertKeyboardEvents,
        widgets=[],
    ),
    "settings" : Mode(
        keyboardEventHandler=settingsKeyboardEvents,
        widgets=[],
    ),
    "help" : Mode(
        keyboardEventHandler=helpKeyboardEvents,
        widgets=[
            Layout(
                screen=screen,
                name="helpToolbar",
                position=[0, 2],
                contents=[
                    Text(
                        screen=screen,
                        text=" "
                    ),
                    Button(
                        screen=screen,
                        name="prev",
                        text="<"
                    ),
                    Expander(screen=screen),
                    Text(
                        screen=screen,
                        name="sectionName"
                    ),
                    Expander(screen=screen),
                    Button(
                        screen=screen,
                        name="next",
                        text=">"
                    ),
                    Text(
                        screen=screen,
                        text=" "
                    )
                ]
            ),
            HLine(
                screen=screen,
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

def modeButtonsClickHandler(clickType, clickPosition):
    for button in mainToolbar.interactibles:
        button.clickHandler(clickType, clickPosition)
### Events Reactions ###

### Subscribtions ###
subscribe("modeUpdate", onModeUpdate)
subscribe("mouseEvent", modeButtonsClickHandler)
### Subscribtions ###

### Functions ###
def redrawScreen() -> None:
    # global activeMode
    screen.erase()

    mainToolbar.draw()
    HLine(
        screen,
        position=[0, 1],
        expand=True
    ).draw()
    
    activeMode.drawFunction()

def screenResizeCheckerandUpdater() -> list[int, int]:
    minW = screen.getmaxyx()[1] - mainToolbar.size[0]
    minH = screen.getmaxyx()[0] - 15
    
    while minW < 0 or minH < 0:
        minW = screen.getmaxyx()[1] - mainToolbar.size[0] - 2
        minH = screen.getmaxyx()[0] - 15 - 2

        screen.erase()
        screen.addch(0, 0, "")
        screen.refresh()

    redrawScreen()
    
    return screen.getmaxyx()
### Functions ###