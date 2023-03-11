from __future__ import annotations
import curses as nc
import curses.ascii as ac
from signal import signal, SIGINT, SIGTERM
import traceback
import re

import CringeGlobals
from CringeEvents import *


kbKeys = {
    nc.KEY_LEFT : "←",
    nc.KEY_RIGHT : "→",
    nc.KEY_UP : "↑",
    nc.KEY_DOWN : "↓",
    546 : "CTRL+←",
    561 : "CTRL+→",
    573 : "CTRL+↑",
    532 : "CTRL+↓",
    337 : "SHIFT+↑",
    336 : "SHIFT+↓",
    402 : "SHIFT+→",
    393 : "SHIFT+←",
    
    10  : "Return",
    27  : "Esc",
    263 : "Backspace",
    330 : "Del",
}

def initCringeMidi() -> nc._CursesWindow:
    screen = nc.initscr()
    nc.cbreak()
    nc.noecho()
    nc.curs_set(0)
    nc.mouseinterval(0)
    nc.set_escdelay(100)
    screen.keypad(1)

    if nc.has_colors():
        nc.start_color()
        nc.use_default_colors()
        nc.init_pair(CringeGlobals.CRINGE_COLOR_BLUE,  33, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_PRPL, 135, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_DSBL, 245, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_NTRL, 250, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_SHRP, 240, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[0], 196, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[1],  40, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[2],  33, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[3], 200, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[4], 220, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[5],  51, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[6], 202, -1)
        nc.init_pair(CringeGlobals.CRINGE_COLOR_ISTR[7],  99, -1)

    nc.mousemask(-1)
    
    signal(SIGINT, terminationJudgement)
    signal(SIGTERM, terminationJudgement)

    return screen

def terminationJudgement(*_):
    if CringeGlobals.projectSavedStatus:
        endCringeMidi()
    else:
        choice = dialogueChoicePrompt(prompt="Current buffer isn't saved:  [S]ave and Exit   [D]iscard and Exit   [C]ancel", acceptedKeys=["S", "s", "D", "d", "C", "c", "Esc"], attributes=nc.color_pair(CringeGlobals.CRINGE_COLOR_BLUE))
        if choice in ("S", "s"):
            raiseEvent("saveProject")
            endCringeMidi()
        elif choice in ("D", "d"):
            endCringeMidi()

def endCringeMidi() -> None:
    screen.keypad(0)
    nc.curs_set(1)
    nc.nocbreak()
    nc.echo()
    nc.endwin()
    traceback.print_exc()
    exit(0)

def screenResizeCheckerandUpdater():
    while True:
        try:
            raiseEvent("screenResized")
        except:
            screen.erase()
            screen.addch(0, 0, "!")
            screen.refresh()
        else:
            break

def convertKeyboardEvents(keyCode: int) -> str:
    global kbKeys
    if ac.isprint(keyCode):
        return chr(keyCode)
    elif keyCode in kbKeys:
        return kbKeys[keyCode]
    else:
        raise UnhandledKeyCode(f"Keycode {keyCode} is not handled by function convertKeyboardEvents")

def textInputPrompt(prompt: str = "", placeholer:str = "", limit: int = 50, attributes: int = 0) -> str | None:
    string = placeholer
    cursor = len(string)

    while True:
        try:
            screen.addstr(screen.getmaxyx()[0] - 1, 0, " " * (screen.getmaxyx()[1] - 1), attributes | nc.A_REVERSE)
            screen.addstr(screen.getmaxyx()[0] - 1, 0, f" {prompt}{string}", attributes | nc.A_REVERSE)
            screen.chgat(screen.getmaxyx()[0] - 1, len(prompt) + cursor + 1, attributes | nc.A_REVERSE | nc.A_UNDERLINE)
            screen.chgat(screen.getmaxyx()[0] - 1, len(prompt) + cursor + 2, attributes | nc.A_REVERSE)

            event = screen.getch()
            
            if event == nc.KEY_RESIZE:
                screenResizeCheckerandUpdater()
            elif event != -1:
                try:
                    event = convertKeyboardEvents(event)
                    
                    if   event == "Esc":
                        return None
                    elif event == "Return":
                        if not len(string):
                            return None
                        return string
                    elif event == "Backspace" and cursor > 0:
                        string = string[0:cursor-1] + string[cursor:]
                        cursor -= 1
                    elif event == "Del" and cursor < len(string):
                        string = string[0:cursor] + string[cursor+1:]
                    elif re.findall(r"^←$", event) and cursor:
                        cursor -= 1
                    elif re.findall(r"^→$", event) and cursor < len(string):
                        cursor += 1
                    elif (len(string) < limit) and len(event) == 1 and (ord(event) >= 0x20 and ord(event) < 0x7F):
                        if string:
                            string = string[0:cursor] + event + string[cursor:]
                        else:
                            string = event
                        cursor += 1
                except UnhandledKeyCode:
                    pass
        except:
            screen.erase()
            screen.addch(0, 0, "!")
            screen.refresh()

def dialogueChoicePrompt(prompt: str = "?", acceptedKeys: list[str] = ["Return", "y", "Esc", "n"], attributes: int = 0) -> str:
    while True:
        try:
            screen.addstr(screen.getmaxyx()[0] - 1, 0, " " * (screen.getmaxyx()[1] - 1), attributes | nc.A_REVERSE)
            screen.addstr(screen.getmaxyx()[0] - 1, 0, f" {prompt}", attributes | nc.A_REVERSE)
            
            event = screen.getch()
            
            if event == nc.KEY_RESIZE:
                screenResizeCheckerandUpdater()
            elif event != -1:
                try:
                    event = convertKeyboardEvents(event)
                    if event in acceptedKeys:
                        return event
                except UnhandledKeyCode:
                    pass
        except:
            screen.erase()
            screen.addch(0, 0, "!")
            screen.refresh()


screen = initCringeMidi()
subscribe("exit", terminationJudgement)