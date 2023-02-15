from __future__ import annotations
import curses as nc
from abc import ABCMeta, abstractmethod
from random import randint
from CringeEvents import raiseEvent

from CringeGlobals import *
from CringeMisc import *

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
        name: str = generateUID(),
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
                    
class Button(InteractibleWidget):

    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        eventToRaise: str,
        text: str = "Button",
        position: list[int, int] = None,
        size: list[int, int] = None,
        color: int = nc.color_pair(0),
        enabled: bool = True
    ) -> None:

        size = [len(text), 1]
        super().__init__(screen, name, position, size, enabled)

        self.state = False
        self.text = text
        self.color = color
        self.event = eventToRaise

    def __str__(self) -> str:
        return self.text

    def draw(self):
        self.screen.addstr(self.position[1], self.position[0], self.text, self.color)

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
        sizeToFit = maxSize - self.position[self.__layout] - sizeToFit
        
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
        color = nc.color_pair(self.color if self.visible else CRINGE_COLOR_DSBL) | (nc.A_REVERSE if self.selected else 0)
        self.screen.addstr(self.position[1], self.position[0], " " * 20, color)
        self.screen.addstr(self.position[1] + 1, self.position[0], " " * 20, color)
        self.screen.addnstr(self.position[1], self.position[0] + 1, self.name, 18, color)
        self.screen.addstr(self.position[1] + 1, self.position[0] + 1, " " if self.visible else " ", color)
        self.screen.addnstr(self.position[1] + 1, self.position[0] + 5, self.type, 10, color)
        self.screen.addstr(self.position[1] + 1, self.position[0] + 17, "󰴱 ", color)

    def clickHandler(self, clickType: int, clickPosition: list[int, int]) -> str | None:
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
        insTypeList = CRINGE_ISTR_TYPES
        self.type = insTypeList[(insTypeList.index(self.type) + 1) % len(insTypeList)]

    def changeColor(self):
        colorList = CRINGE_COLOR_ISTR
        self.color = colorList[(colorList.index(self.color) + 1) % len(colorList)]
        
    def changeName(self):
        # newName = getInput(prompt="New Name : ", limit=18, attributes=nc.color_pair(self.color) | nc.A_REVERSE)
        # if newName: self.name = newName
        pass
        
    def toggleVisible(self):
        self.visible = not self.visible

class Project(InteractibleWidget):
    
    def __init__(
        self,
        screen: nc._CursesWindow,
        name: str,
        position: list[int, int] = None,
    ) -> None:
        
        size = [screen.getmaxyx()[1], screen.getmaxyx()[0] - position[1] - 1]
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
                    text="--"
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
        self.size = [self.screen.getmaxyx()[1], self.screen.getmaxyx()[0] - self.position[1] - 1]
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
        VLine(screen=self.screen, position=[20, 3], expand=True).draw()
        self.screen.addch(3, 20, "┬")
        self.pad.erase()
        for ins in self.instrumentList:
            ins.draw()

        if self.selectee * 2 < self.instrumentScrollIndex:
            self.instrumentScrollIndex = self.selectee * 2
        elif self.selectee * 2 > self.instrumentScrollIndex + self.size[1] - 3:
            self.instrumentScrollIndex = self.selectee * 2 - self.size[1] + 3

        self.screen.refresh()
        self.pad.refresh(
            self.instrumentScrollIndex,
            0,
            self.position[1] + 1,
            self.position[0],
            self.position[1] + self.size[1],
            self.position[0] + self.size[0]
        )
    
    def clickHandler(self, clickType: int, clickPosition: list[int, int]) -> str | None:
        for w in self.toolbar.interactibles:
            if w.clickHandler(clickType, clickPosition):
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
                        if ins.clickHandler(clickType, [relPos[0] - 1, relPos[1] + self.instrumentScrollIndex - 1]):
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
        self.instrumentList.append(Instrument(screen=self.pad, color=randint(CRINGE_COLOR_ISTR[0], CRINGE_COLOR_ISTR[-1])))
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
