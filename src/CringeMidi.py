class Note():
    
    def __init__(self, note:str=None, length:int=1, volume:int=4) -> None:
        self.note = note
        self.length = length
        self.volume = volume

class Instrument():
    
    def __init__(self, name="New Instrument", type="sine", visible=True) -> None:
        self.notes = []
        self.name = name
        self.type = type
        self.visible = visible

    def __str__(self) -> str:
        return self.name

class Sheet():
    
    def __init__(self) -> None:
        self.instruments = []
