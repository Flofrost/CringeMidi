subscribers = dict()
lastEvent = ""
lastUncaughtEvent = ""

scheduledEvents = dict()
tickTimestamp = 0

def subscribe(event: str, responseFunction):
    if not event in subscribers:
        subscribers[event] = list()
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
        

def schedule(name: str, function, delay: int, persistent: bool = False, *data):
    global tickTimestamp, scheduledEvents

    scheduledEvents[name] = {
        "function": function,
        "date": tickTimestamp,
        "delay": delay,
        "persistent": persistent,
        "data": data
    }

def unschedule(name: str):
    global scheduledEvents

    if name in scheduledEvents:
        scheduledEvents.pop(name)

def runScheduler():
    global tickTimestamp, scheduledEvents

    toUnschedule = list()

    for eventName, event in scheduledEvents.items():
        if tickTimestamp - event["date"] > event["delay"]:
            event["function"](*event["data"])
            if event["persistent"]:
                event["date"] = tickTimestamp
            else:
                toUnschedule.append(eventName)
                
    for eventName in toUnschedule:
        unschedule(eventName)

    tickTimestamp += 1
    

class IncorrectNoteFormat(Exception):
    ...
    
class UnhandledKeyCode(Exception):
    ...

class ScreenTooSmall(Exception):
    ...