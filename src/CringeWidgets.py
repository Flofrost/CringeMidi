from __future__ import annotations
import curses as nc
from abc import ABCMeta, abstractmethod

from CringeMidi import *
from CringeMisc import *

def drawAllWidgetsIn(widgetList:list[Widget]) -> None:
    for w in widgetList:
        w.draw()

class Widget(metaclass=ABCMeta):

    def __init__(self,
                 screen:nc._CursesWindow,
                 name:str,
                 position: list[int, int] = None,
                 size: list[int, int] = None) -> None:
        
        self.screen = screen
        self.name = name
        self.position = [0, 0] if position is None else position
        self.size = [1, 1] if size is None else size
        
    @abstractmethod
    def draw(self):
        pass
    
class InteractibleWidget(Widget, metaclass=ABCMeta):
    
    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str,
                 position: list[int, int] = None,
                 respondsTo: int = nc.BUTTON1_CLICKED,
                 size: list[int, int] = None,
                 enabled: bool = True) -> None:
        
        super().__init__(screen, name, position, size)

        self.respondsTo = respondsTo
        self.enabled = enabled
        
    @abstractmethod
    def clicked(self, clickType:int, clickPosition:list[int, int]) -> bool:
        pass

class Expander(Widget):
    
    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str = generateUID(),
                 filler: str = " ",
                 position: list[int, int] = None,
                 size: list[int, int] = None) -> None:
        super().__init__(screen, name, position, size)
        
        self.filler = filler

    def __str__(self) -> str:
        return self.filler * self.size[0]
    
    def draw(self):
        self.screen.addstr(self.position[1], self.position[0], str(self))

class Line(Widget):

    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str = generateUID(),
                 position: list[int, int] = None,
                 size: list[int, int] = None,
                 color: int = 0) -> None:
        
        if (size[0] == 1 or size[1] == 1) and not (size[0] == 1 and size[1] == 1):
            self.size = size
            self.__dir = False if size[0] == 1 else True
        else:
            raise Exception("Size does not describe a stricly horizontal or vertical line")

        super().__init__(screen, name, position, size)
        
        self.color = color
        
    def draw(self):
        if self.__dir:
            for i in range(self.size[0]):
                relPos = self.position[0] + i
                if chr(self.screen.inch(self.position[1], relPos)) == "│":
                    self.screen.addch(self.position[1], relPos, "┼", nc.color_pair(self.color))
                else:
                    self.screen.addch(self.position[1], relPos, "─", nc.color_pair(self.color))
        else:
            for j in range(self.size[1]):
                relPos = self.position[1] + j
                if chr(self.screen.inch(relPos, self.position[0])) == "─":
                    self.screen.addch(relPos, self.position[0], "┼", nc.color_pair(self.color))
                else:
                    self.screen.addch(relPos, self.position[0], "│", nc.color_pair(self.color))
                    
class Button(InteractibleWidget):

    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str,
                 text: str = "Button",
                 position: list[int, int] = None,
                 respondsTo: int = nc.BUTTON1_CLICKED,
                 size: list[int, int] = None,
                 style: str = "text",
                 color: int = 0,
                 enabled: bool = True) -> None:

        if style == "text":
            size = [len(text), 1]
        elif style == "bordered":
            size = [len(text) + 2, 3]
        else:
            raise Exception(f"'{style}' is not a recognized style")

        super().__init__(screen, name, position, respondsTo, size, enabled)

        self.text = text
        self.style = style
        self.color = color
        self.respondsTo = respondsTo

    def __str__(self) -> str:
        return self.text

    def draw(self):
        if self.style == "text":
            self.screen.addstr(self.position[1], self.position[0], self.text, nc.color_pair(self.color))
        elif self.style == "bordered":
            topbot = "─" * len(self.text)
            self.screen.addstr(self.position[1], self.position[0], "┌" + topbot + "┐", nc.color_pair(self.color))
            self.screen.addstr(self.position[1] + 1, self.position[0], "│" + self.text + "│", nc.color_pair(self.color))
            self.screen.addstr(self.position[1] + 2, self.position[0], "└" + topbot + "┘", nc.color_pair(self.color))

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        if self.enabled and clickType == self.respondsTo:
            relPos = subPos(clickPosition, self.position)
            if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
                return True
        return False

class ToggleButton(Button):

    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str,
                 text: str = "Button",
                 position: list[int, int] = None,
                 size: list[int, int] = None,
                 respondsTo: int = nc.BUTTON1_CLICKED,
                 style: str = "text",
                 color: int = 0,
                 enabled: bool = True) -> None:

        super().__init__(screen, name, text, position, respondsTo, size, style, color, enabled)

        self.state = False
        
    def draw(self):
        color = (nc.color_pair(self.color) | nc.A_REVERSE) if self.state else nc.color_pair(self.color)
        if self.style == "text":
            self.screen.addstr(self.position[1], self.position[0], self.text, color)
        elif self.style == "bordered":
            topbot = "─" * len(self.text)
            self.screen.addstr(self.position[1], self.position[0], "┌" + topbot + "┐", color)
            self.screen.addstr(self.position[1] + 1, self.position[0], "│" + self.text + "│", color)
            self.screen.addstr(self.position[1] + 2, self.position[0], "└" + topbot + "┘", color)

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        if self.enabled and clickType == self.respondsTo:
            relPos = subPos(clickPosition, self.position)
            if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
                self.state = not self.state
                self.draw()
                return True
        return False
    
class Toolbar(Widget):

    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str,
                 contents: list[Widget],
                 position: list[int, int] = None,
                 layoutVertical: bool = False) -> None:
        
        size = 0
        for w in contents:
            size += w.size[int(layoutVertical)]
                
        size = [0, size] if layoutVertical else [size, 0]

        super().__init__(screen, name, position, size)
        
        self.contents = contents
        self.__layout = layoutVertical
        
        self.updateWidgetsPosition()
        
    def draw(self):
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
            sizeToFit += w.size[int(self.__layout)]
        sizeToFit = self.screen.getmaxyx()[int(not self.__layout)] - sizeToFit
            
        expantionSize = sizeToFit // len(listOfExpanders)
        for w in listOfExpanders:
            w.size[0] = expantionSize
                
    def updateWidgetsPosition(self):
        self.calculateExpanders()
        self.contents[0].position = self.position

        for i in range(1,len(self.contents)):
            self.contents[i].position[int(self.__layout)] = self.contents[i-1].position[int(self.__layout)] + self.contents[i-1].size[int(self.__layout)]

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

    def __init__(self, 
                 screen: nc._CursesWindow,
                 text: str = "",
                 justification: str = "left",
                 color: int = 0) -> None:
        
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
