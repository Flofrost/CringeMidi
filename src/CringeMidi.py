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

        super().__init__(screen, name, None, nc.BUTTON1_PRESSED, [20,2], True)

        self.notes = []
        self.type = insType
        self.visible = visible
        
    def draw(self) -> None:
        pass

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


class Sheet():
    
    def __init__(self) -> None:
        pass
