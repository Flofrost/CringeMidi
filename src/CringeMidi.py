import re

freqencyTable = {"C":32.703, "D":36.708, "E":41.203, "F":43.654, "G":48.999, "A":55, "B":61.735}

class Note():
    
    def __init__(self, note:str=None, length:int=1, volume:int=4) -> None:
        self.note = note
        self.length = length
        self.volume = volume

    @staticmethod
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
        
        octave = re.search("\d",noteStr).group(0)
        note = re.search("[A-G#b]{0,2}(?=\d)",noteStr).group(0)
        
        if len(note) > 1:
            if note[1] == "#":
                note = freqencyTable[note[0]] * (2 ** (1/12))
            else:
                note = freqencyTable[note[0]] / (2 ** (1/12))
        else:
            note = freqencyTable[note]
            
        note *= 2 ** (int(octave) - 1)
        
        return note

class Instrument():
    
    def __init__(self) -> None:
        self.notes = []

class Sheet():
    
    def __init__(self) -> None:
        self.instruments = []
