from __future__ import annotations
import curses as nc

from CringeWidgets import *
from CringeMisc import subPos

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

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        relPos = subPos(clickPosition, self.position)
        if (clickType == nc.BUTTON1_PRESSED) and (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
            if self.selected:
                if relPos[0] in [1,2] and relPos[1] == 1:
                    self.visible = not self.visible
                elif relPos[0] in [17,18] and relPos[1] == 1:
                    colorList = CringeGlobals.CRINGE_COLOR_ISTR
                    self.color = colorList[(colorList.index(self.color) + 1) % len(colorList)]
                elif relPos[0] > 3 and relPos[0] < 16 and relPos[1] == 1:
                    insTypeList = CringeGlobals.CRINGE_ISTR_TYPES
                    self.type = insTypeList[(insTypeList.index(self.type) + 1) % len(insTypeList)]
                self.draw()
            return True
        return False
    
class InstrumentList(InteractibleWidget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        position: list[int, int] = None,
    ) -> None:
        
        size = [21, screen.getmaxyx()[0] - position[1] - 1]
        super().__init__(screen, name, position, size, True)

        self.pad: nc._CursesWindow = nc.newpad(20,20)
        self.instrumentList: list[Instrument] = [Instrument(screen=self.pad)]
        self.scrollIndex: int = 0
        self.selectee: int = 0
        
    def updateWidgetsPosition(self):
        self.size = [21, self.screen.getmaxyx()[0] - self.position[1] - 1]
        for i, ins in enumerate(self.instrumentList):
            ins.position = [0, i * 2]
            ins.selected = True if i == self.selectee else False

    def draw(self) -> None:
        self.updateWidgetsPosition()

        for ins in self.instrumentList:
            ins.draw()

        self.screen.refresh()
        self.pad.refresh(
            self.scrollIndex,
            0,
            self.position[1],
            self.position[0] + 1,
            self.position[1] + self.size[1],
            self.position[0] + self.size[0]
        )
    
    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        relPos = subPos(clickPosition, self.position)
        if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
            if relPos[0] >= 1:
                for i, ins in enumerate(self.instrumentList):
                    if ins.clicked(clickType, [relPos[0] -1, relPos[1] + self.scrollIndex]):
                        self.selectee = i
            self.draw()
            
    def addInstrument(self):
        self.instrumentList.append(Instrument(screen=self.pad))
        if len(self.instrumentList) > self.pad.getmaxyx()[0] // 2:
            self.pad.resize(len(self.instrumentList) * 2 + 6, 20)
        self.draw()

class Sheet():
    
    def __init__(self) -> None:
        pass
