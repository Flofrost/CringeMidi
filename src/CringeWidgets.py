from __future__ import annotations
import curses as nc
from abc import ABCMeta, abstractmethod
from random import randint
from CringeEvents import raiseEvent
import json

from CringeGlobals import *
from CringeMisc import *

#                  0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
lineComponents = ("•", "↓", "→", "┘", "↑", "│", "┐", "┤", "←", "└", "─", "┴", "┌", "├", "┬", "┼")

class Widget(metaclass=ABCMeta):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
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
    def clickHandler(self, clickType:int, clickPosition:list[int, int]) -> None:
        pass

class Expander(Widget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = generateUID(),
        filler: str = "⠀",
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
        name: str = generateUID(),
        position: list[int, int] = None,
        size: int = None,
        expand: bool = False,
        color: int = 0
    ) -> None:
        
        super().__init__(screen, name, position, size)

        if expand:
            self.size = [screen.getmaxyx()[1] - self.position[0], 1]
        else:
            self.size = [size, 1]
        
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

        posToFix = []
        for i in range(self.size[0]):
            col = self.position[0] + i
            if chr(screen.inch(self.position[1], col)) == "┼":
                index = 0
                if self.position[1] > 0 and chr(screen.inch(self.position[1] - 1, col)) in ("┼", "│"):
                    index += 1
                if col > 0 and chr(screen.inch(self.position[1], col - 1)) in ("┼", "─"):
                    index += 2
                if self.position[1] < screen.getmaxyx()[0] - 1 and chr(screen.inch(self.position[1] + 1, col)) in ("┼", "│"):
                    index += 4
                if col < screen.getmaxyx()[1] - 1 and chr(screen.inch(self.position[1], col + 1)) in ("┼", "─"):
                    index += 8
                posToFix.append([self.position[1], col, lineComponents[index]])

        for p in posToFix:
            self.screen.addch(p[0], p[1], p[2], nc.color_pair(self.color))

class VLine(Widget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = generateUID(),
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
        
        posToFix = []
        for j in range(self.size[1]):
            row = self.position[1] + j
            if chr(screen.inch(row, self.position[0])) == "┼":
                index = 0
                if row > 0 and chr(screen.inch(row - 1, self.position[0])) in ("┼", "│"):
                    index += 1
                if self.position[0] > 0 and chr(screen.inch(row, self.position[0] - 1)) in ("┼", "─"):
                    index += 2
                if row < screen.getmaxyx()[0] - 1 and chr(screen.inch(row + 1, self.position[0])) in ("┼", "│"):
                    index += 4
                if self.position[0] < screen.getmaxyx()[1] - 1 and chr(screen.inch(row, self.position[0] + 1)) in ("┼", "─"):
                    index += 8
                posToFix.append([row, self.position[0], lineComponents[index]])

        for p in posToFix:
            self.screen.addch(p[0], p[1], p[2], nc.color_pair(self.color))
                    
class Text(Widget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = generateUID(),
        text: str = "Text",
        position: list[int, int] = None,
        color: int = 0
    ) -> None:

        self.text = text
        self.color = color

        super().__init__(screen, name, position, [len(self.text), 1])
    
    def draw(self) -> None:
        self.screen.addstr(self.position[1], self.position[0], self.text, nc.color_pair(self.color))
        
    def changeText(self, newText: str):
        self.text = newText
        self.size = [len(self.text), 1]
                    
class LargeText(InteractibleWidget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        text: list[str],
        position: list[int, int] = None,
        size: list[int, int] = None,
        ) -> None:

        super().__init__(screen, name, position, size, True)
        
        self.text = text
        self.pad = nc.newpad(self.calcPadLength(), self.size[0])
        self.scrollIndex = 0
        
    def draw(self) -> None:
        self.pad.erase()
        
        index = 0
        for text in self.text:
            linesTaken = len(text) // self.size[0]
            if linesTaken:
                for i in range(linesTaken + 1):
                    self.pad.addnstr(index, 0, text[self.size[0] * i:], self.size[0])
                    index += 1
            else:
                self.pad.addstr(index, 0, text)
                index += 1

        self.screen.refresh()
        self.pad.refresh(
            self.scrollIndex, 0,
            self.position[1], self.position[0],
            self.position[1] + self.size[1], self.position[0] + self.size[0],
        )
    
    def clickHandler(self, clickType: int, clickPosition: list[int, int]) -> None:
        relPos = subPos(clickPosition, self.position)
        if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
            if clickType == nc.BUTTON5_PRESSED:
                if self.scrollIndex < self.pad.getmaxyx()[0] - self.size[1]:
                    self.scrollIndex += 1
                self.draw()
            elif clickType == nc.BUTTON4_PRESSED:
                if self.scrollIndex > 0:
                    self.scrollIndex -= 1
                self.draw()
                    
    def calcPadLength(self) -> int:
        totalLength = 0
        for text in self.text:
            totalLength += 1 + (len(text) // self.size[0])
        if totalLength < self.size[1]:
            totalLength = self.size[1]
        return totalLength

    def resize(self, newSize: list[int, int]) -> None:
        self.size = newSize
        self.pad.resize(self.calcPadLength(), self.size[0])
        
    def changeText(self, newText: list[str]) -> None:
        self.text = newText
        self.pad.resize(self.calcPadLength(), self.size[0])
        self.draw()

class Button(InteractibleWidget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        eventToRaise: str = None,
        text: str = "Button",
        position: list[int, int] = None,
        size: list[int, int] = None,
        color: int = nc.color_pair(0),
        enabled: bool = True
    ) -> None:

        size = [len(text), 1]
        super().__init__(screen, name, position, size, enabled)

        self.text = text
        self.color = color
        self.event = eventToRaise if eventToRaise else name

    def __str__(self) -> str:
        return self.text

    def draw(self):
        color = self.color if self.enabled else nc.color_pair(CRINGE_COLOR_DSBL)
        self.screen.addstr(self.position[1], self.position[0], self.text, color)

    def clickHandler(self, clickType: int, clickPosition: list[int, int]) -> None:
        if self.enabled and clickType == nc.BUTTON1_PRESSED:
            relPos = subPos(clickPosition, self.position)
            if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
                raiseEvent(self.event, self)

class Layout(Widget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        contents: list[Widget],
        position: list[int, int] = None,
        layoutVertical: bool = False,
        maxSize: int = None
    ) -> None:

        if not maxSize:
            size = 0
            for w in contents:
                size += w.size[int(layoutVertical)]
                    
            size = [1, size] if layoutVertical else [size, 1]
        else:
            size = [1, maxSize] if layoutVertical else [maxSize, 1]

        super().__init__(screen, name, position, size)
        
        self.contents = contents
        self.maxSize = maxSize
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
        maxSize = self.maxSize if self.maxSize else self.screen.getmaxyx()[1 - self.__layout]
        sizeToFit = maxSize - sizeToFit
        
        if sizeToFit < 0:
            raise Exception(f"Can't fit all elements in available real estate {self.name}")
            
        expantionSize = sizeToFit // len(listOfExpanders)
        for w in listOfExpanders:
            w.size[0] = expantionSize
                
    def updateWidgetsPosition(self):
        self.calculateExpanders()
        self.contents[0].position = self.position

        for i in range(1,len(self.contents)):
            self.contents[i].position[self.__layout] = self.contents[i-1].position[self.__layout] + self.contents[i-1].size[self.__layout]
            self.contents[i].position[1 - self.__layout] = self.position[1 - self.__layout]
    
    def getWidget(self, name: str) -> Widget:
        for w in self.contents:
            if w.name == name:
                return w
        raise Exception(f"No widget with name {name}")

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
        color: int = 0
    ) -> None:
        
        self.screen = screen
        self.text = ["", ""]
        self.color = color
        
    def draw(self):
        self.position = [0, self.screen.getmaxyx()[0]-1]
        self.screen.addstr(self.position[1], self.position[0], " " * (self.screen.getmaxyx()[1] - 1), nc.color_pair(self.color) | nc.A_REVERSE)

        self.screen.addstr(self.position[1], self.position[0], self.text[0], nc.color_pair(self.color) | nc.A_REVERSE)
        self.screen.addstr(self.position[1], self.screen.getmaxyx()[1] - len(self.text[1]) - 1, self.text[1], nc.color_pair(self.color) | nc.A_REVERSE)
        
    def updateText(self,textL: str = "", textR: str = ""):
        self.text = [textL, textR]
        self.draw()

class Instrument():
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str = "New Instrument",
        insType: str = "sine",
        visible: bool = True,
        color: int = 10,
        notes: list[int] = None
    ) -> None:

        self.screen = screen
        self.name = name
        self.position = [0, 0]
        self.size = [20, 2]
        self.notes: list[int] = notes if notes else [0,0,0,0,5,5,5,5,5,5,5,60,60,60,60,60,10,10,10,10,10,10,10,10]
        self.type = insType
        self.visible = visible
        self.selected = False
        self.color = color
        
    def __str__(self) -> str:
        pass
        
    def draw(self) -> None:
        color = nc.color_pair(self.color if self.visible else CRINGE_COLOR_DSBL) | (nc.A_REVERSE if self.selected else 0)
        self.screen.addstr(self.position[1], self.position[0], " " * 20, color)
        self.screen.addstr(self.position[1] + 1, self.position[0], " " * 20, color)
        self.screen.addnstr(self.position[1], self.position[0] + 1, self.name, 18, color)
        self.screen.addstr(self.position[1] + 1, self.position[0] + 1, " " if self.visible else " ", color)
        self.screen.addnstr(self.position[1] + 1, self.position[0] + 5, self.type, 10, color)
        self.screen.addstr(self.position[1] + 1, self.position[0] + 17, "󰴱 ", color)

    def isClicked(self, clickType: int, clickPosition: list[int, int]) -> bool:
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
            return True
        return False
    
    def changeType(self):
        insTypeList = CRINGE_ISTR_TYPES
        self.type = insTypeList[(insTypeList.index(self.type) + 1) % len(insTypeList)]
        raiseEvent("saveState")

    def changeColor(self):
        colorList = CRINGE_COLOR_ISTR
        self.color = colorList[(colorList.index(self.color) + 1) % len(colorList)]
        raiseEvent("saveState")
        
    def changeName(self):
        newName = getInput(prompt="New Name : ", limit=18, attributes=nc.color_pair(self.color) | nc.A_REVERSE)
        if newName:
            self.name = newName
            raiseEvent("saveState")
        
    def toggleVisible(self):
        self.visible = not self.visible
        raiseEvent("saveState")

    def encode(self) -> dict:
        return {
            "name" : self.name,
            "type" : self.type,
            "visible" : self.visible,
            "color" : self.color,
            "notes" : ",".join(encodeNotes(self.notes))
        }

    def load(self, data: dict) -> Instrument:
        self.name = data["name"]
        self.type = data["type"]
        self.visible = data["visible"]
        self.color = data["color"]
        self.notes = decodeNotes(data["notes"].split(","))
        return self

class Project(InteractibleWidget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        position: list[int, int] = None,
    ) -> None:
        
        size = [screen.getmaxyx()[1], screen.getmaxyx()[0] - position[1] - 1]
        super().__init__(screen, name, position, size, True)


        self.pad: nc._CursesWindow = nc.newpad(21,20)
        self.instrumentList: list[Instrument] = [Instrument(screen=self.pad)]
        self.instrumentScrollIndex: int = 0
        self.selectee: int = 0
        
    def __sizeof__(self) -> int:
        return super().__sizeof__() + sum([ins.__sizeof__() for ins in self.instrumentList])
        
    def updateWidgetsPosition(self):
        self.size = [self.screen.getmaxyx()[1], self.screen.getmaxyx()[0] - self.position[1] - 1]
        for i, ins in enumerate(self.instrumentList):
            ins.position = [0, i * 2]
            ins.selected = True if i == self.selectee else False

    def draw(self) -> None:
        self.updateWidgetsPosition()
        
        self.pad.erase()
        for ins in self.instrumentList:
            ins.draw()

        self.screen.refresh()
        self.pad.refresh(
            self.instrumentScrollIndex,
            0,
            self.position[1],
            self.position[0],
            self.position[1] + self.size[1],
            self.position[0] + self.size[0]
        )
    
    def clickHandler(self, clickType: int, clickPosition: list[int, int]) -> None:
        relPos = subPos(clickPosition, self.position)
        if (relPos[0] >= 0) and (relPos[1] >= 0) and (relPos[0] < self.size[0]) and (relPos[1] < self.size[1]):
            if clickType == nc.BUTTON1_PRESSED:
                for i, ins in enumerate(self.instrumentList):
                    if ins.isClicked(clickType, [relPos[0], relPos[1] + self.instrumentScrollIndex]):
                        self.selectee = i
                self.draw()
                raiseEvent("instrumentListUpdate", self)
            elif clickType == nc.BUTTON5_PRESSED:
                if self.instrumentScrollIndex < self.pad.getmaxyx()[0] - self.size[1]:
                    self.instrumentScrollIndex += 1
                self.draw()
                raiseEvent("instrumentListUpdate", self)
            elif clickType == nc.BUTTON4_PRESSED:
                if self.instrumentScrollIndex > 0:
                    self.instrumentScrollIndex -= 1
                self.draw()
                raiseEvent("instrumentListUpdate", self)
            
    def addInstrument(self, *_):
        self.instrumentList.append(Instrument(screen=self.pad, color=randint(CRINGE_COLOR_ISTR[0], CRINGE_COLOR_ISTR[-1])))
        if len(self.instrumentList) + 1 > self.pad.getmaxyx()[0] // 2:
            self.pad.resize(len(self.instrumentList) * 2 + 7, 20)
        self.draw()
        raiseEvent("instrumentListUpdate", self)
        raiseEvent("saveState")
    
    def rmvInstrument(self, *_):
        if len(self.instrumentList) > 1:
            self.instrumentList.remove(self.instrumentList[self.selectee])
            self.selectee = self.selectee % len(self.instrumentList)
            if (self.pad.getmaxyx()[0] // 2) - len(self.instrumentList) > 6:
                self.pad.resize(len(self.instrumentList) * 2 + 7, 20)
            self.draw()
        raiseEvent("instrumentListUpdate", self)
        raiseEvent("saveState")
            
    def selectNext(self, next=True):
        self.selectee = (self.selectee + (1 if next else -1)) % len(self.instrumentList)

        if self.selectee * 2 < self.instrumentScrollIndex:
            self.instrumentScrollIndex = self.selectee * 2
        elif self.selectee * 2 > self.instrumentScrollIndex + self.size[1] - 3:
            self.instrumentScrollIndex = self.selectee * 2 - self.size[1] + 3

        self.draw()
        
    def uppInstrument(self, *_):
        if self.selectee > 0:
            ins = self.instrumentList.pop(self.selectee)
            self.selectee -= 1
            self.instrumentList.insert(self.selectee, ins)
            self.draw()
        raiseEvent("instrumentListUpdate", self)
        raiseEvent("saveState")
            
    def dwnInstrument(self, *_):
        if self.selectee < len(self.instrumentList) - 1:
            ins = self.instrumentList.pop(self.selectee)
            self.selectee += 1
            self.instrumentList.insert(self.selectee, ins)
            self.draw()
        raiseEvent("instrumentListUpdate", self)
        raiseEvent("saveState")
        
    def changeInstrument(self, thingToChange: str):
        if   thingToChange == "visible":
            self.selectedInstrument.toggleVisible()
        elif thingToChange == "name":
            self.selectedInstrument.changeName()
        elif thingToChange == "type":
            self.selectedInstrument.changeType()
        elif thingToChange == "color":
            self.selectedInstrument.changeColor()
        self.draw()

    def save(self, pretty=False) -> str:
        instList = [i.encode() for i in self.instrumentList]

        d = {
            "selectee" : self.selectee,
            "instrumentList" : instList
        }

        return json.dumps(d, indent=4 if pretty else None)

    def load(self, data: str):
        d = json.loads(data)

        self.selectee = d["selectee"]

        self.pad.resize(len(d["instrumentList"]) * 2 + 3, 20)
        self.instrumentList = [Instrument(screen=self.pad).load(ins) for ins in d["instrumentList"]]

    @property
    def selectedInstrument(self) -> Instrument:
        return self.instrumentList[self.selectee]
