import CringeModes

activeMode = "normal"

modes = {
    "normal": {
        "initFunction" : CringeModes.initNormalMode,
        "drawFunction" : CringeModes.drawNormalMode,
        "eventHandler" : CringeModes.handleNormalModeEvents
    },
    "insert": {
        "initFunction" : CringeModes.initInsertMode,
        "drawFunction" : CringeModes.drawInsertMode,
        "eventHandler" : CringeModes.handleInsertModeEvents
    }
}

debugInfo = ""
lastEvent = ""
