import CringeModes

CRINGE_COLOR_BLUE = 1
CRINGE_COLOR_PRPL = 2
CRINGE_COLOR_DSBL = 3

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
    },
    "help": {
        "initFunction" : CringeModes.initHelpMode,
        "drawFunction" : CringeModes.drawHelpMode,
        "eventHandler" : CringeModes.handleHelpModeEvents
    }
}

debugInfo = ""
lastEvent = ""
