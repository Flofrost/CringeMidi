from __future__ import annotations
import curses as nc
from abc import ABCMeta, abstractmethod
from turtle import st

from CringeMidi import *
from CringeMisc import *

class Widget(metaclass=ABCMeta):

    def __init__(self,
                 screen:nc._CursesWindow,
                 name:str,
                 position: list[int, int] = [0,0],
                 color: int = 0) -> None:
        
        self.screen = screen
        self.name = name
        self.position = position
        self.color = color
        
    @abstractmethod
    def draw(self):
        pass
    
class InteractibleWidget(Widget, metaclass=ABCMeta):
    
    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str,
                 position: list[int, int] = [0, 0],
                 respondsTo: int = nc.BUTTON1_CLICKED,
                 color: int = 0) -> None:

        super().__init__(screen, name, position, color)

        self.respondsTo = respondsTo
        
    @abstractmethod
    def clicked(self, clickType:int, clickPosition:list[int, int]) -> bool:
        pass

class ToggleButton(InteractibleWidget):

    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str,
                 position: list[int, int] = [0, 0],
                 respondsTo: int = nc.BUTTON1_CLICKED,
                 text: str = "Button",
                 style: str = "text",
                 color: int = 0) -> None:

        super().__init__(screen, name, position, respondsTo, color)

        if style == "text":
            size = [len(text), 1]
        elif style == "bordered":
            size = [len(text) + 2, 3]
        else:
            raise Exception(f"'{style}' is not a recognized style")

        self.size = size 
        self.text = text
        self.style = style
        self.color = color
        self.respondsTo = respondsTo
        self.state = False
        
        self.draw()
        
    def draw(self):
        color = (self.color | nc.A_REVERSE) if self.state else self.color
        if self.style == "text":
            self.screen.addstr(self.position[1], self.position[0], self.text, color)
        elif self.style == "bordered":
            topbot = "─" * len(self.text)
            self.screen.addstr(self.position[1], self.position[0], "┌" + topbot + "┐", color)
            self.screen.addstr(self.position[1] + 1, self.position[0], "│" + self.text + "│", color)
            self.screen.addstr(self.position[1] + 2, self.position[0], "└" + topbot + "┘", color)

    def clicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
        if clickType == self.respondsTo:
            relPos = subPos(clickPosition, self.position)
            if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
                self.state = not self.state
                self.draw()
                return True
        return False
    
class StatusBar(Widget):

    def __init__(self, 
                 screen: nc._CursesWindow,
                 name: str,
                 position: list[int, int] = [0, 0],
                 text: str = "",
                 justification: str = "left",
                 color: int = 0) -> None:
        
        super().__init__(screen, name, position, color)

        self.text = text
        self.color = color
        self.justification = justification
        
        self.draw()
        
    def draw(self):
        self.position = [0, self.screen.getmaxyx()[0]-1]
        self.screen.move(self.position[1], self.position[0])
        self.screen.clrtoeol()

        if self.justification == "left":
            text = self.text + " " * (self.screen.getmaxyx()[1] - len(self.text) - 1)
            self.screen.addstr(self.position[1], self.position[0], text, nc.color_pair(self.color) | nc.A_REVERSE)
        elif self.justification == "center":
            textMid = len(self.text) // 2
            screenMid = self.screen.getmaxyx()[1] // 2
            text = " " * (screenMid - textMid - 1) + self.text + " " * (screenMid - textMid - 1)
            self.screen.addstr(self.position[1], 0, text, nc.color_pair(self.color) | nc.A_REVERSE)
        
    def updateText(self,text: str):
        self.text = text
        self.draw()
