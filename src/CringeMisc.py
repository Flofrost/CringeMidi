from random import randint
import re

### Lookup Tables ###
freqencyTable = {"C":32.703, "D":36.708, "E":41.203, "F":43.654, "G":48.999, "A":55, "B":61.735}
noteTable = [
    "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
    "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
    "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
    "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
    "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
    "S", "S", "S", "S"
]
volumeTable = ["F", "f", "p", "P"]
### Lookup Tables ###

    
### Note Encoding and Decoding ###
def encodeNote(count: int, note: int) -> str:
    if (note & 0x3f) >= 60: # If the note is silence
        volumeStr = ""
        noteStr = "S"
    else:
        volumeStr = f"{volumeTable[note >> 6]}"
        noteStr = f"{noteTable[note & 0x3F]}"

    return f"{count}{noteStr}{volumeStr}"

def decodeNote(noteString: str) -> list[int]:
    if re.findall("\d+S", noteString): # is note silence
        return [60] * int(re.findall("\d+", noteString)[0])
    else:
        components = re.findall("(\d+)([A-G]#?[2-6])([FfpP])", noteString)
        if not components:
            raise Exception("Incorrect note format")
        count  = components[0][0]
        note   = components[0][1]
        volume = components[0][2]
        return [noteTable.index(note) + (volumeTable.index(volume) << 6)] * int(count)

def encodeNotes(notes: list[int]) -> list[str]:
    if not notes: return list()

    index = 1
    combo = 1
    prev = notes[0]
    output = list()

    while index < len(notes):
        if notes[index] != prev:
            output.append(encodeNote(combo, prev))
            combo = 0
            prev = notes[index]
        index += 1
        combo += 1

    output.append(encodeNote(combo, prev))
    return output
            
def decodeNotes(notes: list[str]) -> list[int]:
    try:
        output = list()
        for note in notes:
            output.extend(decodeNote(note))
        return output
    except:
        return list()
### Note Encoding and Decoding ###


### Misc ###
def regexTest(pattern: str, s: str, outputList: list[str] = None) -> bool:
    r = re.findall(pattern, s)
    if r:
        outputList[0] = r
        return True
    return False

def generateUID() -> str:
    return "".join([chr(randint(0x20, 0x7E)) for i in range(16)])

def subPos(a: list[int, int], b: list[int, int]) -> list[int, int]:
    return [a[0] - b[0], a[1] - b[1]]
### Misc ###

