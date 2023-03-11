from CringeEvents import *

CRINGE_COLOR_BLUE = 1
CRINGE_COLOR_PRPL = 2
CRINGE_COLOR_DSBL = 3
CRINGE_COLOR_NTRL = 4
CRINGE_COLOR_SHRP = 5
CRINGE_COLOR_ISTR = [10, 11, 12, 13, 14, 15, 16, 17]

CRINGE_ISTR_TYPES = [
    "sine",
    "square",
    "triangle",
    "noise"
]

debugInfo = ""
commandCombo = ""
projectSavedStatus = "󱣫 "
scheduledSaveStateStatus = ""


helpContents = [
    ["Normal Mode Commands", [
        "Icon | Keys          Name - Description",
        "     |",
        "    | i             Insert - Goes to the begening of the note and enters Insert mode",
        "    | H             Help - Goes to this screen (Help screen)",
        "     | :             Command - Input a command",
        "     |",
        " 󰕍   | u             Undo - Undoes last action or last inserting session",
        " 󰑏   | r             Redo - Undoes an Undo, Redo list gets cleared when new actions are performed",
        "     |",
        "     |               Pan the sheet",
        "     |",
        "     | j or 󰘶 +     Select - Selects the next Instrument (can also click on the Instrument)",
        "     | k or 󰘶 +     Select - Selects the previous Instrument (can also click on the Instrument)",
        "    | ma            Add Instrument - Append an Instrument to the Project",
        "    | md            Remove Instrument - Remove the selected Instrument from the Project",
        "    | Ctrl+        Move Instrument Up - Raises the selected Instrument in the Instrument list",
        "    | Ctrl+        Move Instrument Down - Lowers the selected Instrument in the Instrument list",
        "     | mr            Rename Instrument - Changes the Instrument's name",
        "    | mv            Toggle Visibility - Toggles wether the Instrument is included in playback and export",
        "     | mt            Change Instrument Type - Changes what the Instrument sounds like",
        " 󰴱   | mc            Change Instrument Color - Changes the Instrument color",
    ]],
    ["Status Bar", [
        "Icon | Name - Description",
        "     |",
        "    | Command Combo - Currently active command combo, cleared when valid command is reached or with Esc or Return",
        " 󱣫   | Save State - This icon appears after the file is save or freshly opened, and no modifications occured",
        " 󱫍   | State Uncached - Every actions performed while this icon is present will be part of the same undo/redo batch. Press Esc, Return, or undo to force the chaching",
    ]],
    ["Commands", [
        "Command(s)          | Name - Description",
        "                    |",
        "w, write, save      | Save Project - Save project to it's location",
        "q, quit, exit       | Quit - Exit CringeMidi, if the project is unsaved, will prompt whether to save or discard it first",
        "wq                  | Write and Quit - Saves project then quits",
        "                    |",
        "log, debug          | Debug Mode - Accesses logs for debugging purposes",
    ]]
]

debugContents = [
    ["Log", [
    ]]
]

def log(logEntry: str):
    global debugContents
    debugContents[0][1].append(logEntry)
subscribe("log", log)