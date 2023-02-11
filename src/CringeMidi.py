from __future__ import annotations
import curses as nc

from CringeWidgets import *

class Instrument(InteractibleWidget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        insType: str = "sine",
        visible: bool = True,
        color: int = 10
    ) -> None:

        super().__init__(screen, name, None, [20,2], True)

        self.notes = []
        self.type = insType
        self.visible = visible
        self.selected = False
        
    def draw(self) -> None:
        color = nc.color_pair(self.color if self.selected else CringeGlobals.CRINGE_COLOR_DSBL) | nc.A_REVERSE
        self.screen.addstr(self.position[1], self.position[0], " " * 20)
        self.screen.addstr(self.position[1] + 1, self.position[0], " " * 20)

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        return False
    
class InstrumentList(Widget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        position: list[int, int] = None,
        size: list[int, int] = None
    ) -> None:

        super().__init__(screen, name, position, size)

        self.instrumentList: list[Instrument] = [Instrument(screen=screen, name="Ins1")]
        self.instrumentList[0].position = [0, 4]
        
    def draw(self) -> None:
       for ins in self.instrumentList:
        ins.draw()

class Sheet():
    
    def __init__(self) -> None:
        pass
