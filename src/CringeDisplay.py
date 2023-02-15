import curses as nc
from CringeEvents import *
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

# project = Project(
#     screen=screen,
#     name="instrumentList",
#     position=[0, 4]
# )

statusBar = StatusBar(
    screen=screen,
    color=CRINGE_COLOR_PRPL
)
### Global ###

### Normal ###
### Normal ###

### Insert ###
### Insert ###

### Settings ###
### Settings ###

### Help ###
### Help ###

### Events Reactions ###
def onModeUpdate(newMode: str | Widget):
    if isinstance(newMode, Widget):
        newMode = newMode.name
    for modeButton in mainToolbar.interactibles:
        if modeButton.name == newMode:
            modeButton.color = modeButton.color | nc.A_REVERSE
        else:
            modeButton.color = modeButton.color & ~(nc.A_REVERSE)
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
def getInput(prompt: str = "", limit: int = 50, attributes: int = 0) -> str | None:
    screen.timeout(-1)
    
    string = ""
    while True:
        screen.addstr(screen.getmaxyx()[0] - 1, 0, " " * (screen.getmaxyx()[1] - 1), attributes)
        screen.addstr(screen.getmaxyx()[0] - 1, 0, f" {prompt}{string}_", attributes)

        event = screen.getkey()
        if event == "\x1b": # Escape
            string = None
            break
        elif event == "\n": # Return
            if not len(string):
                string = None
            break
        elif event == "KEY_BACKSPACE": # Backspace
            if len(string) > 1:
                string = string[:len(string)-1]
            else:
                string = ""
        elif event.isprintable() and len(event) == 1:
            if len(string) < limit:
                string += event
    screen.timeout(20)

    return string

def fixDecorativeLines():
    posToFix = []
    for row in range(screen.getmaxyx()[0]):
        for col in range(screen.getmaxyx()[1]):
            if chr(screen.inch(row, col)) == "┼":
                index = 0
                if row > 0 and chr(screen.inch(row - 1, col)) in ("┼", "│"):
                    index += 1
                if col > 0 and chr(screen.inch(row, col - 1)) in ("┼", "─"):
                    index += 2
                if row < screen.getmaxyx()[0] - 1 and chr(screen.inch(row + 1, col)) in ("┼", "│"):
                    index += 4
                if col < screen.getmaxyx()[1] - 1 and chr(screen.inch(row, col + 1)) in ("┼", "─"):
                    index += 8
                posToFix.append([row, col, index])
                
    for p in posToFix:
        #                        0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
        screen.addch(p[0], p[1], (" ", " ", " ", "┘", " ", "│", "┐", "┤", " ", "└", "─", "┴", "┌", "├", "┬", "┼")[p[2]])

def redrawScreen() -> None:
    screen.erase()

    mainToolbar.draw()
    HLine(
        screen,
        position=[0, 1],
        expand=True
    ).draw()
    
    # CringeGlobals.activeMode.drawFunction()

    fixDecorativeLines()

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