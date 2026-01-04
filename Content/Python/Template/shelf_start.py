from . import shelf_main as _main
#from TATools.ToolShelf import shelf_core
from . import (
                shelf_core,
                shelf_utl,
                ue_utl,
                shelf_utl_widgets,
                )
import importlib
import os
import unreal
import pathlib
import sys
# add parent path to sys.path

# UMGWIDGET = None
os.environ["shelf_debug"] = "False"
shelf_utl.extend_python_path()

def start(show=True):
    # global UMGWIDGET

    if shelf_utl.get_is_debug():
        #importlib.reload(shelf_core)
        importlib.reload(shelf_utl)
        importlib.reload(ue_utl)
        shelf_utl.register_all_stack_handle(True)
        importlib.reload(_main)
        if shelf_core.UMGWIDGET:
            del shelf_core.UMGWIDGET
            import gc
            gc.collect()
        shelf_core.UMGWIDGET = _main.CGTeamWorkWindow()
        shelf_core.UMGWIDGET.setup()
    else:
        if not shelf_core.UMGWIDGET:
            shelf_utl.register_all_stack_handle(False)
            shelf_core.UMGWIDGET = _main.CGTeamWorkWindow()
            shelf_core.UMGWIDGET.setup()
    if show:
        unreal.PythonWidgetExtendLib.spawn_and_register_tab("Tool Shelf", "Tool Shelf", shelf_core.UMGWIDGET.main_layout)

