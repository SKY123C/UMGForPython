from . import shelf_main as _main
from . import (
                shelf_core,
                shelf_utl,
                shelf_utl_widgets,
                )
import importlib
import os
import unreal

UMGWIDGET = None
os.environ["tw_debug"] = "False"
shelf_utl.extend_python_path()

def start(show=True):
    global UMGWIDGET
    
    if os.environ.get("tw_debug") == "True":
        #importlib.reload(shelf_core)
        importlib.reload(shelf_utl)
        importlib.reload(shelf_utl_widgets)
        shelf_utl.register_all_stack_handle(True)
        importlib.reload(_main)
        if UMGWIDGET:
            del UMGWIDGET
            import gc
            gc.collect()
        UMGWIDGET = _main.CGTeamWorkWindow()
    else:
        if not UMGWIDGET:
            shelf_utl.register_all_stack_handle(False)
            UMGWIDGET = _main.CGTeamWorkWindow()
    if show:
        unreal.PythonWidgetExtendLib.spawn_and_register_tab("Tool Shelf", "Tool Shelf", UMGWIDGET.main_layout)
