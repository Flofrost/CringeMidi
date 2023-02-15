subscribers = dict()
lastEvent = ""

def subscribe(event: str, responseFunction):
    if not event in subscribers:
        subscribers[event] = []
    subscribers[event].append(responseFunction)
    
def raiseEvent(event: str, *data):
    global lastEvent
    if not event in ("mouseEvent", "keyboardEvent"): lastEvent = event

    if not event in subscribers:
        return
    for responseFunction in subscribers[event]:
        responseFunction(*data)