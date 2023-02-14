from __future__ import annotations
import curses as nc
from random import randint

import CringeGlobals
from CringeMisc import subPos
from CringeWidgets import *
from CringeDisplay import *

class Instrument(InteractibleWidget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = "New Instrument",
        insType: str = "sine",
        visible: bool = True,
        color: int = 10
    ) -> None:

        super().__init__(screen, name, None, [20,2], True)

        self.notes = []
        self.type = insType
        self.visible = visible
        self.selected = False
        self.color = color
        
    def draw(self) -> None:
        color = nc.color_pair(self.color if self.visible else CringeGlobals.CRINGE_COLOR_DSBL) | (nc.A_REVERSE if self.selected else 0)
        self.screen.addstr(self.position[1], self.position[0], " " * 20, color)
        self.screen.addstr(self.position[1] + 1, self.position[0], " " * 20, color)
        self.screen.addnstr(self.position[1], self.position[0] + 1, self.name, 18, color)
        self.screen.addstr(self.position[1] + 1, self.position[0] + 1, " " if self.visible else " ", color)
        self.screen.addnstr(self.position[1] + 1, self.position[0] + 5, self.type, 10, color)
        self.screen.addstr(self.position[1] + 1, self.position[0] + 17, "󰴱 ", color)

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> str | None:
        relPos = subPos(clickPosition, self.position)
        if (clickType == nc.BUTTON1_PRESSED) and (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
            if self.selected:
                if relPos[0] in [1,2] and relPos[1] == 1:
                    self.toggleVisible()
                elif relPos[0] in [17,18] and relPos[1] == 1:
                    self.changeColor()
                elif relPos[0] > 3 and relPos[0] < 16 and relPos[1] == 1:
                    self.changeType()
                elif relPos[0] > 1 and relPos[0] < 17 and relPos[1] == 0:
                    self.changeName()
            return self.name
    
    def changeType(self):
        insTypeList = CringeGlobals.CRINGE_ISTR_TYPES
        self.type = insTypeList[(insTypeList.index(self.type) + 1) % len(insTypeList)]

    def changeColor(self):
        colorList = CringeGlobals.CRINGE_COLOR_ISTR
        self.color = colorList[(colorList.index(self.color) + 1) % len(colorList)]
        
    def changeName(self):
        newName = getInput(prompt="New Name : ", limit=18, attributes=nc.color_pair(self.color) | nc.A_REVERSE)
        if newName: self.name = newName
        
    def toggleVisible(self):
        self.visible = not self.visible

class Sheet(InteractibleWidget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        position: list[int, int] = None,
    ) -> None:
        
        size = [21, screen.getmaxyx()[0] - position[1] - 1]
        super().__init__(screen, name, position, size, True)

        self.toolbar: Layout = Layout(
            screen=screen,
            name="instrumentToolbar",
            position=self.position,
            maxSize=21,
            contents=[
                Expander(
                    screen=screen,
                    filler="-"
                ),
                Button(
                    screen=screen,
                    name="addInstrument",
                    text=" "
                ),
                Text(
                    screen=screen,
                    text="--"
                ),
                Button(
                    screen=screen,
                    name="rmvInstrument",
                    text=" ",
                    enabled=False
                ),
                Text(
                    screen=screen,
                    text="---"
                ),
                Button(
                    screen=screen,
                    name="uppInstrument",
                    text=" ",
                    enabled=False
                ),
                Text(
                    screen=screen,
                    text="--"
                ),
                Button(
                    screen=screen,
                    name="dwnInstrument",
                    text=" ",
                    enabled=False
                ),
                Expander(
                    screen=screen,
                    filler="-"
                )
            ]
        )

        self.pad: nc._CursesWindow = nc.newpad(21,20)
        self.instrumentList: list[Instrument] = [Instrument(screen=self.pad)]
        self.instrumentScrollIndex: int = 0
        self.selectee: int = 0
        
    def updateWidgetsPosition(self):
        self.size = [21, self.screen.getmaxyx()[0] - self.position[1] - 1]
        for i, ins in enumerate(self.instrumentList):
            ins.position = [0, i * 2]
            ins.selected = True if i == self.selectee else False

    def updateToolbar(self):
        self.toolbar.contents[3].enabled = True if len(self.instrumentList) > 1 else False
        self.toolbar.contents[5].enabled = True if self.selectee > 0 else False
        self.toolbar.contents[7].enabled = True if self.selectee < len(self.instrumentList) - 1 else False

    def draw(self) -> None:
        self.updateToolbar()
        self.updateWidgetsPosition()
        
        self.toolbar.draw()
        HLine(screen=self.screen, position=[ 0, 3], expand=True).draw()
        VLine(screen=self.screen, position=[21, 3], expand=True).draw()
        self.screen.addch(3, 21, "┬")
        self.pad.erase()
        for ins in self.instrumentList:
            ins.draw()

        self.screen.refresh()
        self.pad.refresh(
            self.instrumentScrollIndex,
            0,
            self.position[1] + 1,
            self.position[0] + 1,
            self.position[1] + self.size[1],
            self.position[0] + self.size[0]
        )
    
    def clicked(self, clickType: int, clickPosition: list[int, int]) -> str | None:
        for w in self.toolbar.interactibles:
            if w.clicked(clickType, clickPosition):
                if   w.name == "addInstrument":
                    self.addInstrument()
                elif w.name == "rmvInstrument":
                    self.rmvInstrument()
                elif w.name == "uppInstrument":
                    self.move()
                elif w.name == "dwnInstrument":
                    self.move(False)

                return w.name

        relPos = subPos(clickPosition, self.position)
        if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
            if (relPos[0] >= 1) and (relPos[1] >= 1):
                if clickType == nc.BUTTON1_PRESSED:
                    for i, ins in enumerate(self.instrumentList):
                        if ins.clicked(clickType, [relPos[0] - 1, relPos[1] + self.instrumentScrollIndex - 1]):
                            self.selectee = i
                elif clickType == nc.BUTTON5_PRESSED:
                    if self.instrumentScrollIndex < self.pad.getmaxyx()[0] - self.size[1]:
                        self.instrumentScrollIndex += 1
                        self.draw()
                elif clickType == nc.BUTTON4_PRESSED:
                    if self.instrumentScrollIndex > 0:
                        self.instrumentScrollIndex -= 1
                        self.draw()
            self.draw()
            return "intrumentEvent"
            
    def addInstrument(self):
        self.instrumentList.append(Instrument(screen=self.pad, color=randint(CringeGlobals.CRINGE_COLOR_ISTR[0], CringeGlobals.CRINGE_COLOR_ISTR[-1])))
        if len(self.instrumentList) + 1 > self.pad.getmaxyx()[0] // 2:
            self.pad.resize(len(self.instrumentList) * 2 + 7, 20)
        self.draw()
    
    def rmvInstrument(self):
        self.instrumentList.remove(self.instrumentList[self.selectee])
        self.selectee = self.selectee % len(self.instrumentList)
        if (self.pad.getmaxyx()[0] // 2) - len(self.instrumentList) > 6:
            self.pad.resize(len(self.instrumentList) * 2 + 7, 20)
        self.draw()
            
    def selectNext(self, next=True):
        self.selectee = (self.selectee + (1 if next else -1)) % len(self.instrumentList)
        if self.selectee * 2 < self.instrumentScrollIndex:
            self.instrumentScrollIndex = self.selectee * 2
        elif self.selectee * 2 > self.instrumentScrollIndex + self.size[1] - 3:
            self.instrumentScrollIndex = self.selectee * 2 - self.size[1] + 3
        self.draw()
        
    def move(self, up=True):
        if up and self.selectee > 0:
            ins = self.instrumentList.pop(self.selectee)
            self.selectee -= 1
            self.instrumentList.insert(self.selectee, ins)
            self.draw()
        elif not up and self.selectee < len(self.instrumentList) - 1:
            ins = self.instrumentList.pop(self.selectee)
            self.selectee += 1
            self.instrumentList.insert(self.selectee, ins)
            self.draw()

    @property
    def selectedInstrument(self) -> Instrument:
        return self.instrumentList[self.selectee]

### Creation of global widgets ###
CringeGlobals.mainToolbar = Layout(
    screen=screen,
    name="mainToolbar",
    position=[0, 0],
    contents=[
        VLine(
            screen=screen,
            size=2
        ),
        ToggleButton(
            screen=screen,
            name="normal",
            text="󱣱 Normal",
            color=CRINGE_COLOR_BLUE
        ),
        VLine(
            screen=screen,
            size=2
        ),
        ToggleButton(
            screen=screen,
            name="insert",
            text=" Insert",
            color=CRINGE_COLOR_BLUE
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
        ToggleButton(
            screen=screen,
            name="settings",
            text=" Settings",
            color=CRINGE_COLOR_BLUE
        ),
        VLine(
            screen=screen,
            size=2
        ),
        ToggleButton(
            screen=screen,
            name="help",
            text=" Help",
            color=CRINGE_COLOR_BLUE
        ),
        VLine(
            screen=screen,
            size=2
        ),
        Button(
            screen=screen,
            name="exit",
            text=" Exit",
            color=CRINGE_COLOR_BLUE
        ),
        VLine(
            screen=screen,
            size=2
        )
    ]
)

CringeGlobals.mainToolBarLine = HLine(
    screen=screen,
    position=[0, 1],
    expand=True
)

CringeGlobals.sheet = Sheet(
    screen=screen,
    name="instrumentList",
    position=[0, 4]
)

CringeGlobals.statusBar = StatusBar(
    screen=screen,
    color=CRINGE_COLOR_PRPL
)
### Creation of global widgets ###