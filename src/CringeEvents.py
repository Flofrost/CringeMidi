subscribers = dict()
lastEvent = ""
lastUncaughtEvent = ""

def subscribe(event: str, responseFunction):
    if not event in subscribers:
        subscribers[event] = []
    subscribers[event].append(responseFunction)
    
def unsubscribe(event: str, responseFunction):
    if not event in subscribers:
        return
    subscribers[event].remove(responseFunction)
    
def raiseEvent(event: str, *data):
    global lastEvent, lastUncaughtEvent

    if not event in subscribers:
        if not event in ("mouseEvent", "keyboardEvent"): lastUncaughtEvent = event
        return

    if not event in ("mouseEvent", "keyboardEvent"): lastEvent = event
    for responseFunction in subscribers[event]:
        responseFunction(*data)