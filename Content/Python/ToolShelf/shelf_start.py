from . import shelf_main as _main
from . import (
                shelf_core,
                shelf_utl
                )
import importlib
import os
import unreal
import pathlib
import sys

UMGWIDGET = None
os.environ["tw_debug"] = "False"
def start():
    global UMGWIDGET
    
    if os.environ.get("tw_debug") == "True":
        importlib.reload(shelf_core)
        importlib.reload(shelf_utl)
        shelf_utl.register_all_stack_handle(True)
        importlib.reload(_main)
        UMGWIDGET = _main.CGTeamWorkWindow()
    else:
        if not UMGWIDGET:
            shelf_utl.register_all_stack_handle(False)
            UMGWIDGET = _main.CGTeamWorkWindow()
    unreal.PythonWidgetExtendLib.spawn_and_register_tab("Tool Shelf", "Tool Shelf", UMGWIDGET.main_layout)
