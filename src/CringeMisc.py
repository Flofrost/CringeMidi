from random import randint
import re

freqencyTable = {"C":32.703, "D":36.708, "E":41.203, "F":43.654, "G":48.999, "A":55, "B":61.735}

def generateUID() -> str:
    return "".join([chr(randint(0x20, 0x7E)) for i in range(16)])


def note2freq(noteStr:str) -> float:
    """
    Note format needs to be : XmO\n
    \tX = note from A to G\n
    \tm = sharp as # or flat as b (optionnal)\n
    \tO = octave from 2 to 6\n
    Example:\n
    \tA#6 is A sharp on the 6th octave\n
    \tG5  is G on the 5th octave\n
    Anything else will be considered silence.
    """
    
    try:
        octave = re.search("\d",noteStr).group(0)
        note = re.search("[A-G#b]{0,2}(?=\d)",noteStr).group(0)
        
        if len(note) > 1:
            if note[1] == "#":
                note = freqencyTable[note[0]] * (2 ** (1/12))
            elif note[1] == "b":
                note = freqencyTable[note[0]] / (2 ** (1/12))
        else:
            note = freqencyTable[note]
            
        note *= 2 ** (int(octave) - 1)
    except:
        note = 0
    
    return note

def addPos(a: list[int, int], b: list[int, int]) -> list[int, int]:
    return [a[0] + b[0], a[1] + b[1]]

def subPos(a: list[int, int], b: list[int, int]) -> list[int, int]:
    return [a[0] - b[0], a[1] - b[1]]

def mulPos(a: list[int, int], b: float) -> list[int, int]:
    return [a[0] * b, a[1] * b]

def divPos(a: list[int, int], b: float) -> list[int, int]:
    return [a[0] / b, a[1] / b]