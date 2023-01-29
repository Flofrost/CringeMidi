from __future__ import annotations
import curses as nc
from abc import ABCMeta, abstractmethod

from CringeMidi import *
from CringeMisc import *

class Widget(metaclass=ABCMeta):

    def __init__(self,
                 screen:nc._CursesWindow,
                 name:str=generateUID(),
                 position: list[int, int] = [0,0]) -> None:
        
        self.screen = screen
        self.name = name
        self.position = position
        
    @abstractmethod
    def draw(self):
        pass

class Button(Widget):

    def __init__(self,
                 screen: nc._CursesWindow, 
                 name: str = generateUID(),
                 text: str = "Button",
                 position: list[int, int] = [0, 0],
                 respondsTo: tuple = (nc.BUTTON1_CLICKED,None),
                 style: str = "text") -> None:

        super().__init__(screen, name, position)

        if style == "text":
            size = [len(text), 1]
        else:
            raise Exception(f"'{style}' is not a recognized style")

        self.size = size 
        self.text = text
        self.style = style
        self.respondsTo = respondsTo
        
    def draw(self):
        if self.style == "text":
            self.screen.addstr(self.position[1], self.position[0], self.text)

    def cliked(self, clickPosition:list[int, int], clickType:int) -> bool:
        for response in self.respondsTo:
            if clickType == response:
                relPos = subPos(clickPosition, self.position)
                return (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1])
        return False
    
class StatusBar(Widget):

    def __init__(self,
                 screen: nc._CursesWindow,
                 name: str = generateUID(),
                 text: str = "",
                 color = 0,
                 justification: str = "left") -> None:

        super().__init__(screen, name, [0, screen.getmaxyx()[0]-1])
        
        self.size = [screen.getmaxyx()[1], 1]
        self.text = text
        self.color = color
        self.justification = justification
        
    def draw(self):
        self.position = [0, self.screen.getmaxyx()[0]-1]
        self.screen.move(self.position[1], self.position[0])
        self.screen.clrtoeol()
        self.screen.addstr(self.position[1], self.position[0], self.text, nc.color_pair(self.color))
