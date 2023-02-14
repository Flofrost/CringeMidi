CRINGE_COLOR_BLUE = 1
CRINGE_COLOR_PRPL = 2
CRINGE_COLOR_DSBL = 3
CRINGE_COLOR_ISTR = [10, 11, 12, 13, 14, 15]

CRINGE_ISTR_TYPES = [
    "sine",
    "square",
    "triangle",
    "noise"
]

class EventHandler():

    subscibers = {}
    
    def subscribe(self, event: str, responseFunction, object = None, *args):
        try:
            self.subscibers[event] += [responseFunction, object, args]
        except KeyError:
            self.subscibers[event] = [[responseFunction, object, args]]

    def raiseEvent(self, event: str):
        try:
            for subscriber in self.subscibers[event]:
                subscriber[0](subscriber[1], subscriber[2])
        except KeyError:
            pass

eventHandler = EventHandler()

activeMode      = None
mainToolBar     = None
mainToolBarLine = None
sheet           = None
statusBar       = None

debugInfo = ""
lastEvent = ""
