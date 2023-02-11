from __future__ import annotations
import curses as nc
from abc import ABCMeta, abstractmethod

import CringeGlobals
import CringeMisc

def drawAllWidgetsIn(widgetList:list[Widget]) -> None:
    for w in widgetList:
        w.draw()

class Widget(metaclass=ABCMeta):

    def __init__(
        self,
        screen:nc._CursesWindow,
        name:str,
        position: list[int, int] = None,
        size: list[int, int] = None
    ) -> None:
        
        self.screen = screen
        self.name = name
        self.position = [0, 0] if position is None else position
        self.size = [1, 1] if size is None else size
        
    @abstractmethod
    def draw(self) -> None:
        pass
    
class InteractibleWidget(Widget, metaclass=ABCMeta):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        position: list[int, int] = None,
        size: list[int, int] = None,
        enabled: bool = True
    ) -> None:
        
        super().__init__(screen, name, position, size)

        self.enabled = enabled
        
    @abstractmethod
    def clicked(self, clickType:int, clickPosition:list[int, int]) -> bool:
        pass

class Expander(Widget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = CringeMisc.generateUID(),
        filler: str = " ",
        position: list[int, int] = None
    ) -> None:

        super().__init__(screen, name, position, [0, 0])
        
        self.filler = filler

    def __str__(self) -> str:
        return self.filler * self.size[0]
    
    def draw(self):
        self.screen.addstr(self.position[1], self.position[0], str(self))

class HLine(Widget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = CringeMisc.generateUID(),
        position: list[int, int] = None,
        size: int = None,
        expand: bool = False,
        color: int = 0
    ) -> None:
        
        if expand:
            ssize = [screen.getmaxyx()[1] - position[0], 1]
        else:
            ssize = [size, 1]

        super().__init__(screen, name, position, ssize)
        
        self.color = color
        self.expand = expand
        
    def draw(self):
        if self.expand:
            self.size = [self.screen.getmaxyx()[1] - self.position[0], 1]
        for i in range(self.size[0]):
            relPos = self.position[0] + i
            char = chr(self.screen.inch(self.position[1], relPos))
            if char == "│":
                self.screen.addch(self.position[1], relPos, "┼", nc.color_pair(self.color))
            else:
                self.screen.addch(self.position[1], relPos, "─", nc.color_pair(self.color))
                    
class VLine(Widget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = CringeMisc.generateUID(),
        position: list[int, int] = None,
        size: int = None,
        expand: bool = False,
        color: int = 0
    ) -> None:
        
        if expand:
            ssize = [1, screen.getmaxyx()[0] - position[1]]
        else:
            ssize = [1, size]

        super().__init__(screen, name, position, ssize)
        
        self.color = color
        self.expand = expand
        
    def draw(self):
        if self.expand:
            self.size = [1, self.screen.getmaxyx()[0] - self.position[1]]
        for j in range(self.size[1]):
            relPos = self.position[1] + j
            char = chr(self.screen.inch(relPos, self.position[0]))
            if char == "─":
                self.screen.addch(relPos, self.position[0], "┼", nc.color_pair(self.color))
            else:
                self.screen.addch(relPos, self.position[0], "│", nc.color_pair(self.color))

class Text(Widget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = CringeMisc.generateUID(),
        text: str = "Text",
        position: list[int, int] = None,
        color: int = 0
    ) -> None:

        self.text = text
        self.color = color

        super().__init__(screen, name, position, [len(self.text), 1])
    
    def draw(self) -> None:
        self.screen.addstr(self.position[1], self.position[0], self.text, nc.color_pair(self.color))
                    
class Button(InteractibleWidget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        text: str = "Button",
        position: list[int, int] = None,
        size: list[int, int] = None,
        color: int = 0,
        enabled: bool = True
    ) -> None:

        size = [len(text), 1]
        super().__init__(screen, name, position, size, enabled)

        self.text = text
        self.color = color

    def __str__(self) -> str:
        return self.text

    def draw(self):
        color = nc.color_pair(self.color) if self.enabled else (nc.color_pair(CringeGlobals.CRINGE_COLOR_DSBL))
        self.screen.addstr(self.position[1], self.position[0], self.text, color)

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        if self.enabled and clickType == nc.BUTTON1_PRESSED:
            relPos = CringeMisc.subPos(clickPosition, self.position)
            if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
                return True
        return False

class ToggleButton(Button):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        text: str = "Button",
        position: list[int, int] = None,
        size: list[int, int] = None,
        color: int = 0,
        enabled: bool = True
    ) -> None:

        super().__init__(screen, name, text, position, size, color, enabled)

        self.state = False
        
    def draw(self):
        color = (nc.color_pair(self.color) | nc.A_REVERSE) if self.state else nc.color_pair(self.color)
        self.screen.addstr(self.position[1], self.position[0], self.text, color)

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        if self.enabled and clickType == nc.BUTTON1_PRESSED:
            relPos = CringeMisc.subPos(clickPosition, self.position)
            if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
                self.state = not self.state
                self.draw()
                return True
        return False
    
class Layout(Widget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        contents: list[Widget],
        position: list[int, int] = None,
        layoutVertical: bool = False
    ) -> None:

        size = 0
        for w in contents:
            size += w.size[int(layoutVertical)]
                
        size = [1, size] if layoutVertical else [size, 1]

        super().__init__(screen, name, position, size)
        
        self.contents = contents
        self.__layout = int(layoutVertical)
        
    def draw(self):
        self.updateWidgetsPosition()
        for w in self.contents:
            w.draw()

    def calculateExpanders(self):
        listOfNonExpanders: list[Widget] = []
        listOfExpanders: list[Expander] = []
        for w in self.contents:
            if isinstance(w, Expander):
                listOfExpanders.append(w)
            else:
                listOfNonExpanders.append(w)
                
        if not len(listOfExpanders):
            return
        
        sizeToFit = 0
        for w in listOfNonExpanders:
            sizeToFit += w.size[self.__layout]
        sizeToFit = self.screen.getmaxyx()[1 - self.__layout] - self.position[self.__layout] - sizeToFit
        
        if sizeToFit < 0:
            raise Exception("Can't fit all elements in available real estate")
            
        expantionSize = sizeToFit // len(listOfExpanders)
        for w in listOfExpanders:
            w.size[0] = expantionSize
                
    def updateWidgetsPosition(self):
        self.calculateExpanders()
        self.contents[0].position = self.position

        for i in range(1,len(self.contents)):
            self.contents[i].position[self.__layout] = self.contents[i-1].position[self.__layout] + self.contents[i-1].size[self.__layout]
            self.contents[i].position[1 - self.__layout] = self.position[1 - self.__layout]

    def changeContents(self):
        pass
    
    @property
    def interactibles(self) -> list[InteractibleWidget]:
        listOfInteractibles = []
        for w in self.contents:
            if isinstance(w, InteractibleWidget):
                listOfInteractibles.append(w)
        return listOfInteractibles

class StatusBar():

    def __init__(
        self, 
        screen: nc._CursesWindow,
        text: str = "",
        justification: str = "left",
        color: int = 0
    ) -> None:
        
        self.screen = screen
        self.text = text
        self.color = color
        self.justification = justification
        
    def draw(self):
        self.position = [0, self.screen.getmaxyx()[0]-1]

        if self.justification == "left":
            text = self.text + " " * (self.screen.getmaxyx()[1] - len(self.text) - 1)
            self.screen.addstr(self.position[1], 0, text, nc.color_pair(self.color) | nc.A_REVERSE)
        elif self.justification == "center":
            textMid = len(self.text) // 2
            screenMid = self.screen.getmaxyx()[1] // 2
            text = " " * (screenMid - textMid - 1) + self.text + " " * (screenMid - textMid - 1)
            self.screen.addstr(self.position[1], 0, text, nc.color_pair(self.color) | nc.A_REVERSE)
        
    def updateText(self,text: str):
        self.text = text
        self.draw()
