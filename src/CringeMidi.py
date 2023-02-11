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
        color = nc.color_pair(self.color if self.selected else CringeGlobals.CRINGE_COLOR_DSBL) | nc.A_REVERSE
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
                self.draw()
            return True
        return False
    
class InstrumentList(Layout):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        position: list[int, int] = None,
    ) -> None:
        
        super().__init__(screen, name, [], position, False, None)

        self.instrumentList: list[Instrument] = [Instrument(screen=screen)]
        self.instrumentList[0].position = self.position
        self.instrumentList[0].selected = True
        
    def draw(self) -> None:
       for ins in self.instrumentList:
        ins.draw()
        
    @property
    def interactibles(self) -> list[InteractibleWidget]:
        return self.instrumentList

class Sheet():
    
    def __init__(self) -> None:
        pass
